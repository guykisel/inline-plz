# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os.path

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    {
        "name": "jsonlint",
        "install": [["npm", "install", "jsonlint"]],
        "help": [os.path.normpath("./node_modules/.bin/jsonlint"), "-h"],
        "run": [os.path.normpath("./node_modules/.bin/jsonlint"), "-c", "-q"],
        "rundefault": [os.path.normpath("./node_modules/.bin/jsonlint"), "-c", "-q"],
        "dotfiles": [],
        "language": "json",
        "autorun": True,
        "run_per_file": True,
    }
)
class JSONLintParser(ParserBase):
    """Parse jsonlint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                if file_path.strip() and output.strip():
                    path = file_path
                    line = int(output.split(":")[1].split()[1].strip(", "))
                    msgbody = output
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                print("Invalid message: {0}".format(output))
        return messages
