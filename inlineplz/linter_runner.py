# -*- coding: utf-8 -*-
# pylint: disable=ungrouped-imports,broad-except,too-many-instance-attributes
"""Linter configurations."""

import asyncio
import fnmatch
import multiprocessing
import os.path
import shutil
import sys
import time
import traceback

from identify import identify

from . import linters, message, registry
from .util import system


class LinterRunner:
    def __init__(
        self,
        install=False,
        autorun=False,
        ignore_paths=None,
        config_dir=None,
        enabled_linters=None,
        disabled_linters=None,
        autofix=False,
        trusted=False,
        filenames=None,
    ):
        # TODO: Break this class down with composition or something
        self.install = install
        self.autorun = autorun
        self.autofix = autofix
        self.ignore_paths = ignore_paths or []
        self.config_dir = config_dir or os.getcwd()
        self.config_dir = os.path.abspath(self.config_dir)
        self.fallback_config_dir = os.path.abspath(
            os.path.join(os.path.dirname(linters.__file__), "config")
        )
        self.enabled_linters = enabled_linters or []
        self.disabled_linters = disabled_linters or []
        self.trusted = trusted

        self.all_filenames = self.all_filenames_in_dir(filenames)
        self.path_lock = dict()

        # Keep track of the parsed messages from all of the linters we're running
        self.messages = message.Messages()

        # track commands we've already run so that we don't re-run them
        self.previous_install_commands = []

        # Default event loop is SelectorEventLoop, which on Windows does not support subprocesses
        if sys.platform == "win32":
            self.event_loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(self.event_loop)
        else:
            self.event_loop = asyncio.get_event_loop()

        # Limit the number of concurrent subprocesses we can run to something close to the number of CPUs we have
        self.process_limiter = asyncio.Semaphore(
            value=multiprocessing.cpu_count(), loop=self.event_loop
        )

    async def run_command(  # noqa: MC0001
        self, command, timeout=600, semaphore=None, path=None
    ):
        print("Running command: {}".format(" ".join(command)))
        sys.stdout.flush()

        if not semaphore:
            semaphore = asyncio.Lock(loop=self.event_loop)
        # limit to running one command per file at a time to avoid file handle conflicts
        if path:
            path_lock = self.path_lock.setdefault(
                path, asyncio.Lock(loop=self.event_loop)
            )
        else:
            path_lock = asyncio.Lock(loop=self.event_loop)

        popen_kwargs = {
            "stdout": asyncio.subprocess.PIPE,
            "stderr": asyncio.subprocess.STDOUT,
            "env": os.environ,
        }
        # TODO: Figure out why we don't always get utf-8 back, even on 3.6.X without universal_newlines=True
        if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
            popen_kwargs["encoding"] = "utf-8"

        output = ""
        async with path_lock:
            async with semaphore:
                async with self.process_limiter:
                    if sys.platform == "win32":
                        proc = await asyncio.wait_for(
                            asyncio.create_subprocess_shell(
                                " ".join(command), loop=self.event_loop, **popen_kwargs
                            ),
                            timeout,
                        )
                    else:
                        try:
                            proc = await asyncio.wait_for(
                                asyncio.create_subprocess_exec(
                                    *command, loop=self.event_loop, **popen_kwargs
                                ),
                                timeout,
                            )
                        except FileNotFoundError:
                            print(
                                "{0} unable to execute because command {1} not found in PATH".format(
                                    command, command[0]
                                )
                            )
                            return 1, ""

                    while True:
                        try:
                            line = await asyncio.wait_for(
                                proc.stdout.readline(), timeout
                            )
                            # End of file will return empty
                            if not line:
                                break
                            output += line.decode("utf-8", "replace")
                            continue
                        except asyncio.TimeoutError:
                            print(
                                "{0} timed out in {1} seconds while reading stdout:\n{2}".format(
                                    command, timeout, output
                                )
                            )
                            proc.kill()
                            output = output or ""
                            return 1, output

        try:
            return_code = await asyncio.wait_for(proc.wait(), timeout)
        except asyncio.TimeoutError:
            print(
                "{0} timed out in {1} seconds waiting for process to end:\n{2}".format(
                    command, timeout, output
                )
            )
            proc.kill()
            output = output or ""
            return 1, output

        # TODO: Enable this in verbose logging only
        print("{0}\n{1}\n{0}\n{2}".format("-" * 80, command, output))
        sys.stdout.flush()
        print("{0} returned code {1}".format(command, return_code))
        return return_code, output

    async def performance_hacks(self):
        # https://github.com/npm/npm/issues/11283
        # npm's progress bar makes npm installs much slower
        try:
            await self.run_command(["npm", "set", "progress=false"])
        except Exception:
            pass

    @staticmethod
    def cleanup():
        """Delete standard installation directories."""
        for install_dir in linters.INSTALL_DIRS:
            try:
                shutil.rmtree(install_dir, ignore_errors=True)
            except Exception:
                print(
                    "{0}\nFailed to delete {1}".format(
                        traceback.format_exc(), install_dir
                    )
                )
                sys.stdout.flush()

    def should_ignore_path(self, path):
        for ignore_path in self.ignore_paths:
            if (
                os.path.relpath(path).startswith(ignore_path)
                or path.startswith(ignore_path)
                or fnmatch.fnmatch(path, ignore_path)
                or ignore_path in path.split(os.path.sep)
            ):
                return True

        return False

    async def run_per_file(self, config):
        cmd = self.run_config(config)
        cmds_and_tasks = []
        paths = set()
        per_file_limiter = None
        if config.get("concurrency"):
            per_file_limiter = asyncio.Semaphore(
                value=config["concurrency"], loop=self.event_loop
            )

        for pattern in registry.PATTERNS.get(config.get("language")):
            for filepath in fnmatch.filter(self.all_filenames, pattern):
                if (
                    "text" in identify.tags_from_path(filepath)
                    and filepath not in paths
                ):
                    paths.add(filepath)
                    cmds_and_tasks.append(
                        (
                            cmd + [filepath],
                            asyncio.ensure_future(
                                self.run_command(
                                    cmd + [filepath],
                                    timeout=60,
                                    semaphore=per_file_limiter,
                                    path=filepath,
                                ),
                                loop=self.event_loop,
                            ),
                        )
                    )

        output = []
        for run_cmd, file_task in cmds_and_tasks:
            _, out = await file_task

            # Return the filename and the output
            output.append((run_cmd[-1], out.strip()))

        return output

    def linters_to_run(self):  # noqa: MC0001
        linters = set()
        enabled_linters = self.enabled_linters or []
        disabled_linters = self.disabled_linters or []
        try:
            enabled_linters.extend(enabled_linters[0].split(","))
        except (IndexError, AttributeError):
            pass
        try:
            disabled_linters.extend(disabled_linters[0].split(","))
        except (IndexError, AttributeError):
            pass
        if not (self.autorun or self.autofix):
            for linter, config in registry.LINTERS.items():
                if linter in enabled_linters:
                    linters.add(linter)
        else:
            dotfile_found = set()
            language_found = set()

            # Get the languages
            for linter, config in registry.LINTERS.items():
                if self.dotfiles_exist(config) or self.dotfiles_exist(
                    config, self.config_dir
                ):
                    dotfile_found.add(linter)
                    language_found.add(config.get("language"))

            # Choose what linters we need
            for linter, config in registry.LINTERS.items():
                if linter in disabled_linters:
                    continue

                if linter in enabled_linters:
                    linters.add(linter)
                    continue

                if dotfile_found and config.get("run_if_dotfile_in_root"):
                    linters.add(linter)
                    continue

                if config.get("language") in language_found and (
                    (self.autorun and config.get("autorun"))
                    or (self.autofix and config.get("autofix"))
                ):
                    linters.add(linter)
                    continue

                if self.should_autorun(config):
                    linters.add(linter)

        print("Running with linters: {0}".format(linters))
        return linters

    def all_filenames_in_dir(self, changed_filenames=None):
        # http://stackoverflow.com/a/2186565
        changed_filenames = changed_filenames or set()
        paths = set()
        for root, dirnames, filenames in os.walk(os.getcwd(), topdown=True):
            for ignore in self.ignore_paths:
                try:
                    dirnames.remove(ignore)
                except ValueError:
                    pass
            if self.should_ignore_path(root):
                continue

            for filename in filenames:
                full_path = os.path.join(root, filename)
                if "text" in identify.tags_from_path(full_path):
                    if (
                        changed_filenames
                        and os.path.relpath(os.path.normcase(full_path))
                        .replace("\\", "/")
                        .strip()
                        not in changed_filenames
                    ):
                        continue
                    paths.add(full_path)
        print("Filenames in dir count: {}".format(len(paths)))
        return paths

    def should_autorun(self, config):
        patterns = registry.PATTERNS.get(config.get("language"))
        if (self.autorun and config.get("autorun")) or (
            self.autofix and config.get("autofix")
        ):
            for pattern in patterns:
                if fnmatch.filter(self.all_filenames, pattern):
                    return True

        return False

    @staticmethod
    def dotfiles_exist(config, path=None):
        if path is None:
            path = os.getcwd()
        return any(
            dotfile.strip() in os.listdir(path) for dotfile in config.get("dotfiles")
        )

    async def install_linter(self, config):
        install_cmds = config.get("install")
        linter = config["class"]()
        try:
            linter.install()
        except AttributeError:
            pass
        for install_cmd in install_cmds:
            if await self.installed(config) and not config.get("always_install"):
                return True
            if install_cmd in self.previous_install_commands:
                continue

            self.previous_install_commands.append(install_cmd)
            try:
                await self.run_command(install_cmd)
            except (OSError, asyncio.TimeoutError):
                continue

        return await self.installed(config)

    async def install_trusted(self):
        for install_cmd in linters.TRUSTED_INSTALL:
            try:
                await self.run_command(install_cmd)
            except OSError:
                print(
                    "Trusted install failed: {0}\n{1}".format(
                        install_cmd, traceback.format_exc()
                    )
                )
                sys.stdout.flush()

    async def installed(self, config):
        try:
            returncode, _ = await self.run_command(config.get("help_cmd"))
            return returncode == 0
        except OSError:
            return False

    def run_config(self, config):
        if self.dotfiles_exist(config) and config.get("run"):
            return config.get("run")

        config_dir = self.config_dir
        if not (self.dotfiles_exist(config, self.config_dir)):
            config_dir = self.fallback_config_dir

            if not (self.dotfiles_exist(config, self.fallback_config_dir)):
                print(
                    "Missing default config dotfile for {0}".format(config.get("name"))
                )
                return config.get("run")

        return [
            os.path.normpath(item.format(config_dir=config_dir))
            if "..." not in item
            else item.format(config_dir=config_dir)
            for item in (config.get("rundefault") or config.get("run"))
        ]

    def run_linters(self):  # noqa: MC0001
        self.cleanup()
        linters_to_run = self.linters_to_run()
        self.event_loop.run_until_complete(self.performance_hacks())

        if self.trusted and linters_to_run and (self.install or self.autorun):
            self.event_loop.run_until_complete(self.install_trusted())

        # if the linter can't be run concurrently, just run it immediately
        for linter in linters_to_run:
            config = registry.LINTERS.get(linter)
            if config.get("concurrency", 0) == 1 and not config.get(
                "run_per_file", False
            ):
                self.event_loop.run_until_complete(self.run_linter(linter))

        # now start the rest of the linters
        linter_tasks = []
        for linter in linters_to_run:
            config = registry.LINTERS.get(linter)
            if not (
                config.get("concurrency", 0) == 1
                and not config.get("run_per_file", False)
            ):
                linter_tasks.append(
                    asyncio.ensure_future(self.run_linter(linter), loop=self.event_loop)
                )

        for linter_task in linter_tasks:
            self.event_loop.run_until_complete(linter_task)

        self.event_loop.close()
        return self.messages.get_messages()

    async def run_linter(self, linter):  # noqa: MC0001
        if system.should_stop():
            return

        print("{0}: Linter starting".format(linter))
        sys.stdout.flush()
        output = ""
        config = registry.LINTERS.get(linter)

        start = time.time()
        try:
            if (self.install or self.autorun) and config.get("install"):
                if not await self.install_linter(config):
                    print("Failed to install {0}, skipping.".format(linter))
                    sys.stdout.flush()
                    return
        except OSError:
            print(
                "Install failed, skipping {0}: {1}\n{2}".format(
                    linter, config.get("install"), traceback.format_exc()
                )
            )
            sys.stdout.flush()
            return
        print(
            "Installing {0} took {1} seconds".format(linter, int(time.time() - start))
        )
        sys.stdout.flush()

        start = time.time()
        try:
            if config.get("run_per_file"):
                output = await self.run_per_file(config)
            else:
                cmd = self.run_config(config)
                _, output = await self.run_command(cmd)
        except Exception:
            print("Running {0} failed:\n{1}".format(linter, traceback.format_exc()))
            sys.stdout.flush()
        print(
            "Running of {0} took {1} seconds".format(linter, int(time.time() - start))
        )
        sys.stdout.flush()

        start = time.time()
        try:
            if output:
                linter_messages = config.get("parser")().parse(output)
                # prepend linter name to message content
                linter_messages = {
                    (msg[0], msg[1], "{0}: {1}".format(linter, msg[2]))
                    for msg in linter_messages
                    if not self.should_ignore_path(msg[0]) and msg[2].strip()
                }
                print(
                    "Found {0} messages from {1}".format(len(linter_messages), linter)
                )
                sys.stdout.flush()
                self.messages.add_messages(linter_messages)
        except Exception:
            print(
                "Parsing {0} output failed:\n{1}\n{2}".format(
                    linter, traceback.format_exc(), output
                )
            )
            sys.stdout.flush()
        print(
            "Parsing of {0} took {1} seconds".format(linter, int(time.time() - start))
        )
        sys.stdout.flush()
