# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="proselint",
    install=[[sys.executable, "-m", "pip", "install", "-U", "proselint"]],
    help_cmd=["proselint", "-h"],
    run=["proselint"],
    rundefault=["proselint"],
    dotfiles=[],
    language="text",
    autorun=True,
    run_per_file=True,
    concurrency=1,
)
class ProselintParser(ParserBase):
    """Parse proselint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                if file_path.strip() and output.strip():
                    for line in output.split("\n"):
                        parts = line.split(":")
                        line = int(parts[1].strip())
                        msgbody = ":".join(parts[2:]).strip()
                        messages.add((file_path, line, msgbody))
            except (ValueError, IndexError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, output))
        return messages
