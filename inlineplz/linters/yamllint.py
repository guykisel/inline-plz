# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import sys

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="yamllint",
    install=[[sys.executable, "-m", "pip", "install", "yamllint"]],
    help_cmd=["yamllint", "-h"],
    run=["yamllint", "-f", "parsable", "."],
    rundefault=["yamllint", "-c", "{config_dir}/.yamllint", "-f", "parsable", "."],
    dotfiles=[".yamllint"],
    language="yaml",
    autorun=True,
    run_per_file=False,
)
class YAMLLintParser(ParserBase):
    """Parse yaml-lint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split("\n"):
            try:
                if line.strip():
                    parts = line.split(":")
                    path = parts[0].strip()
                    line = int(parts[1].strip())
                    msgbody = parts[3].strip()
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError, TypeError):
                print("Invalid message: {0}".format(lint_data))
        return messages
