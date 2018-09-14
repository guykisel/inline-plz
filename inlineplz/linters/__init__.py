# -*- coding: utf-8 -*-
# pylint: disable=W0703,C0412
"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
from multiprocessing.pool import ThreadPool as Pool
import os.path
import shutil
import sys
import time
import traceback

from inlineplz.util.system import run_command, install_linter
from inlineplz.registry import get_linters, get_patterns, register_pattern

from identify import identify

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk  # noqa

from inlineplz import message
from inlineplz.util import system

# import your linter here
from inlineplz.linters.ansiblelint import AnsibleLintParser  # NOQA
from inlineplz.linters.bandit import BanditParser  # NOQA
from inlineplz.linters.codenarc import CodenarcParser  # NOQA
from inlineplz.linters.detectsecrets import DetectSecretsParser  # NOQA
from inlineplz.linters.dockerfilelint import DockerfileLintParser  # NOQA
from inlineplz.linters.eclint import ECLintParser  # NOQA
from inlineplz.linters.eslint import ESLintParser  # NOQA
from inlineplz.linters.gherkinlint import GherkinLintParser  # NOQA
from inlineplz.linters.gometalinter import GometalinterParser  # NOQA
from inlineplz.linters.htmlhint import HTMLHintParser  # NOQA
from inlineplz.linters.jscs import JSCSParser  # NOQA
from inlineplz.linters.jshint import JSHintParser  # NOQA
from inlineplz.linters.jsonlint import JSONLintParser  # NOQA
from inlineplz.linters.markdownlint import MarkdownLintParser  # NOQA
from inlineplz.linters.megacheck import MegacheckParser  # NOQA
from inlineplz.linters.pmd import PMDParser  # NOQA
from inlineplz.linters.proselint import ProselintParser  # NOQA
from inlineplz.linters.prospector import ProspectorParser  # NOQA
from inlineplz.linters.rflint import RobotFrameworkLintParser  # NOQA
from inlineplz.linters.rstlint import RSTLintParser  # NOQA
from inlineplz.linters.shellcheck import ShellcheckParser  # NOQA
from inlineplz.linters.spotbugsmaven import SpotbugsMavenParser  # NOQA
from inlineplz.linters.stylint import StylintParser  # NOQA
from inlineplz.linters.tflint import TFLintParser  # NOQA
from inlineplz.linters.yamllint import YAMLLintParser  # NOQA

HERE = os.path.dirname(__file__)


if sys.platform == "win32":
    JAVA_SEP = ";"
else:
    JAVA_SEP = ":"


def vendored_path(path):
    # we use a relpath on windows because the colon in windows drive letter paths messes with java classpaths
    if sys.platform == "win32":
        return os.path.normpath(
            os.path.relpath(
                os.path.join(os.path.dirname(HERE), "bin", path), os.getcwd()
            )
        )

    return os.path.normpath(
        os.path.abspath(os.path.join(os.path.dirname(HERE), "bin", path))
    )


def register_patterns():
    register_pattern("all", ["*.*"])
    register_pattern("ansible", ["*.yaml", "*.yml"])
    register_pattern("docker", ["*Dockerfile", "*.dockerfile"])
    register_pattern("gherkin", ["*.feature"])
    register_pattern("go", ["*.go"])
    register_pattern("groovy", ["*.groovy", "Jenkinsfile", "jenkinsfile"])
    register_pattern("java", ["*.java"])
    register_pattern("javascript", ["*.js"])
    register_pattern("json", ["*.json"])
    register_pattern("html", ["*.html", "*.htm"])
    register_pattern("markdown", ["*.md"])
    register_pattern("python", ["*.py"])
    register_pattern("shell", ["*.sh", "*.zsh", "*.ksh", "*.bsh", "*.csh", "*.bash"])
    register_pattern("stylus", ["*.styl"])
    register_pattern("robotframework", ["*.robot"])
    register_pattern("rst", ["*.rst"])
    register_pattern(
        "text", ["*.md", "*.txt", "*.rtf", "*.html", "*.tex", "*.markdown"]
    )
    register_pattern("yaml", ["*.yaml", "*.yml"])


def init():
    register_patterns()


# TODO: can we not do this at "compile" or "import" time?
init()


def run_config(config, config_dir):
    if dotfiles_exist(config) and config.get("run"):
        return config.get("run")

    if not (config_dir and dotfiles_exist(config, config_dir)):
        config_dir = os.path.abspath(os.path.join(HERE, "config"))
    return [
        os.path.normpath(item.format(config_dir=config_dir))
        if "..." not in item
        else item.format(config_dir=config_dir)
        for item in (config.get("rundefault") or config.get("run"))
    ]


def dotfiles_exist(config, path=None):
    path = path or os.getcwd()
    return any(
        dotfile.strip() in os.listdir(path) for dotfile in config.get("dotfiles")
    )


# these commands will be autorun to try to install dependencies.
TRUSTED_INSTALL = [
    ["bundle", "install"],
    ["cabal", "update"],
    ["cabal", "install"],
    ["glide", "install", "--strip-vendor"],
    ["godep", "get"],
    ["godep", "restore"],
    ["dep", "ensure"],
    ["dep", "prune"],
    ["govendor", "sync"],
    ["go", "get", "-t", "-v", "./..."],
    ["yarn", "install", "--non-interactive"],
    ["npm", "install"],
    [sys.executable, "setup.py", "develop"],
    [sys.executable, "-m", "pip", "install", "."],
    [sys.executable, "-m", "pip", "install", "-e", "."],
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    [sys.executable, "-m", "pip", "install", "-r", "requirements_dev.txt"],
    [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
    ["pipenv", "install"],
]

# these dirs will get deleted after a run
INSTALL_DIRS = ["node_modules", ".bundle"]


def performance_hacks():
    # https://github.com/npm/npm/issues/11283
    # npm's progress bar makes npm installs much slower
    try:
        run_command(["npm", "set", "progress=false"])
    except Exception:
        pass


def cleanup():
    """Delete standard installation directories."""
    for install_dir in INSTALL_DIRS:
        try:
            shutil.rmtree(install_dir, ignore_errors=True)
        except Exception:
            print(traceback.format_exc())
            print("Failed to delete {}".format(install_dir))


def should_ignore_path(path, ignore_paths):
    for ignore_path in ignore_paths:
        if (
            os.path.relpath(path).startswith(ignore_path)
            or path.startswith(ignore_path)
            or fnmatch.fnmatch(path, ignore_path)
            or ignore_path in path.split(os.path.sep)
        ):
            return True

    return False


def run_per_file(config, ignore_paths=None, path=None, config_dir=None):
    ignore_paths = ignore_paths or []
    path = path or os.getcwd()
    cmd = run_config(config, config_dir)
    run_cmds = []
    patterns = get_patterns().get(config.get("language"))
    concurrency = config.get("concurrency")
    paths = all_filenames_in_dir(path=path, ignore_paths=ignore_paths)
    for pattern in patterns:
        for filepath in fnmatch.filter(paths, pattern):
            if "text" in identify.tags_from_path(filepath):
                run_cmds.append(cmd + [filepath])
    pool = Pool(processes=concurrency)

    def result(run_cmd):
        _, out = run_command(run_cmd, timeout=5)
        return run_cmd[-1], out.strip()

    output = pool.map(result, run_cmds)
    return output


def linters_to_run(
    autorun=False, ignore_paths=None, enabled_linters=None, disabled_linters=None
):
    linters = set()
    enabled_linters = enabled_linters or []
    disabled_linters = disabled_linters or []
    try:
        enabled_linters.extend(enabled_linters[0].split(","))
    except (IndexError, AttributeError):
        pass
    try:
        disabled_linters.extend(disabled_linters[0].split(","))
    except (IndexError, AttributeError):
        pass
    if not autorun:
        for linter, config in get_linters().items():
            if linter in enabled_linters:
                linters.add(linter)
    else:
        dotfilefound = {}
        for linter, config in get_linters().items():
            if dotfiles_exist(config):
                dotfilefound[config.get("language")] = True
                if (
                    config.get("run_if_dotfile_in_root")
                    and linter not in disabled_linters
                ):
                    linters.add(linter)
            if dotfilefound.get(config.get("language")) and config.get("autorun"):
                if linter not in disabled_linters:
                    linters.add(linter)
        filenames = all_filenames_in_dir(path=os.getcwd(), ignore_paths=ignore_paths)
        for linter, config in get_linters().items():
            if linter in enabled_linters or (
                not dotfilefound.get(config.get("language"))
                and should_autorun(config, filenames)
            ):
                if linter not in disabled_linters:
                    linters.add(linter)
    return linters


def all_filenames_in_dir(path=None, ignore_paths=None):
    path = path or os.getcwd()
    # http://stackoverflow.com/a/2186565
    paths = set()
    for root, dirnames, filenames in os.walk(path, topdown=True):
        try:
            for ignore in ignore_paths:
                dirnames.remove(ignore)
        except ValueError:
            pass
        if should_ignore_path(root, ignore_paths):
            continue

        for filename in filenames:
            full_path = os.path.join(root, filename)
            if "text" in identify.tags_from_path(full_path):
                paths.add(full_path)
    return paths


def should_autorun(config, filenames):
    patterns = get_patterns().get(config.get("language"))
    if config.get("autorun"):
        for pattern in patterns:
            if fnmatch.filter(filenames, pattern):
                return True

    return False


def install_trusted():
    for install_cmd in TRUSTED_INSTALL:
        try:
            print("*" * 80)
            run_command(install_cmd, log_all=True)
        except OSError:
            print(
                "Install failed: {0}\n{1}".format(install_cmd, traceback.format_exc())
            )


def lint(
    install=False,
    autorun=False,
    ignore_paths=None,
    config_dir=None,
    enabled_linters=None,
    disabled_linters=None,
    trusted=False,
):
    messages = message.Messages()
    cleanup()
    performance_hacks()
    if trusted and (install or autorun):
        install_trusted()
    for linter in linters_to_run(
        autorun, ignore_paths, enabled_linters, disabled_linters
    ):
        if system.should_stop():
            return messages.get_messages()

        print("=" * 80)
        print("Running linter: {0}".format(linter))
        sys.stdout.flush()
        start = time.time()
        output = ""
        config = get_linters().get(linter)
        try:
            if (install or autorun) and config.get("install"):
                install_linter(config)
            if config.get("run_per_file"):
                output = run_per_file(config, ignore_paths, config_dir)
            else:
                cmd = run_config(config, config_dir)
                _, output = run_command(cmd)
                output = output.strip()
        except Exception:
            print("Running {0} failed:".format(linter))
            print(traceback.format_exc())
            print("Failed {0} output: {1}".format(linter, output))
        print(
            "Installation and running of {0} took {1} seconds".format(
                linter, int(time.time() - start)
            )
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
                    if not should_ignore_path(msg[0], ignore_paths)
                }
                print(
                    "Found {0} messages from {1}".format(len(linter_messages), linter)
                )
                messages.add_messages(linter_messages)
        except Exception:
            print("Parsing {0} output failed:".format(linter))
            print(traceback.format_exc())
            print(output)
        print(
            "Parsing of {0} took {1} seconds".format(linter, int(time.time() - start))
        )
    return messages.get_messages()
