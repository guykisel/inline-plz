# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="restructuredtext_lint",
    install=[[sys.executable, "-m", "pip", "install", "-U", "restructuredtext_lint"]],
    help_cmd=["rst-lint", "-h"],
    run=["rst-lint", "--format", "json", "--encoding", "utf-8"],
    rundefault=["rst-lint", "--format", "json", "--encoding", "utf-8"],
    dotfiles=[],
    language="rst",
    autorun=True,
    run_per_file=True,
)
class RSTLintParser(ParserBase):
    """Parse json rst-lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                for msgdata in json.loads(output):
                    try:
                        path = file_path
                        line = msgdata["line"]
                        msgbody = msgdata["message"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print("Invalid message: {0}".format(msgdata))
            except json.error.Error:
                print("Invalid message: {0}".format(output))
        return messages
