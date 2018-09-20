# -*- coding: utf-8 -*-

import sys

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="robotframework-lint",
    install=[[sys.executable, "-m", "pip", "install", "-U", "robotframework-lint"]],
    help_cmd=["rflint", "--help"],
    run=["rflint"],
    rundefault=["rflint", "-A", "{config_dir}/.rflint"],
    dotfiles=[".rflint"],
    language="robotframework",
    autorun=True,
    run_per_file=True,
)
class RobotFrameworkLintParser(ParserBase):
    """Parse rflint output."""

    def parse(self, lint_data):
        messages = set()
        current_file = None
        for _, output in lint_data:
            for line in output.split("\n"):
                try:
                    if not line.strip():
                        continue

                    if line.startswith("+"):
                        current_file = line[2:]
                        continue

                    else:
                        _, position, message = line.split(":")
                        line_number, _ = position.split(",")
                        messages.add(
                            (current_file.strip(), int(line_number), message.strip())
                        )
                except (ValueError, IndexError):
                    print(
                        "({0}) Invalid message: {1}".format(type(self).__name__, line)
                    )
        return messages
