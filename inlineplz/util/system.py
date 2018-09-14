# -*- coding: utf-8 -*-

"""
System utilities
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import traceback
import os
import sys


if sys.version_info >= (3, 5):
    import subprocess
else:
    import subprocess32 as subprocess


STOP_FILE_NAME = ".inlineplzstop"
# track commands we've already run so that we don't re-run them
PREVIOUS_INSTALL_COMMANDS = []


def should_stop():
    return os.path.isfile(os.path.join(os.getcwd(), STOP_FILE_NAME))


def run_command(command, log_on_fail=False, log_all=False, timeout=120):
    print('Running: "{}"'.format(" ".join(command)))
    shell = False
    if os.name == "nt":
        shell = True
    popen_kwargs = {
        "args": command,
        "stdin": subprocess.PIPE,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "shell": shell,
        "env": os.environ,
        "universal_newlines": True,
        "timeout": timeout,
    }
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
        popen_kwargs["encoding"] = "utf-8"
    try:
        proc = subprocess.run(**popen_kwargs)
    except subprocess.TimeoutExpired:
        print("Timeout: {}".format(command))
        return 0, ""

    stdout, stderr = proc.stdout, proc.stderr
    output = "{}\n{}".format(stdout, stderr).strip()
    if output and ((log_on_fail and proc.returncode) or log_all):
        print(output)
        sys.stdout.flush()
    return proc.returncode, output


def installed(config):
    try:
        returncode, _ = run_command(config.get("help"))
        return returncode == 0

    except (subprocess.CalledProcessError, OSError):
        return False


def install_linter(config):
    install_cmds = config.get("install")
    for install_cmd in install_cmds:
        if install_cmd in PREVIOUS_INSTALL_COMMANDS:
            continue

        PREVIOUS_INSTALL_COMMANDS.append(install_cmd)
        if not installed(config):
            try:
                print("-" * 80)
                run_command(install_cmd, log_all=True)
            except OSError:
                print(
                    "Install failed: {0}\n{1}".format(
                        install_cmd, traceback.format_exc()
                    )
                )
        else:
            return


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
