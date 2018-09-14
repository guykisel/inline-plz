# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os.path
from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    {
        "name": "eclint",
        "install": [["npm", "install", "eclint"]],
        "help": [os.path.normpath("./node_modules/.bin/eclint"), "-h"],
        "run": [os.path.normpath("./node_modules/.bin/eclint"), "check"],
        "rundefault": [os.path.normpath("./node_modules/.bin/eclint"), "check"],
        "dotfiles": [".editorconfig"],
        "language": "all",
        "autorun": False,
        "run_per_file": True,
        "run_if_dotfile_in_root": False,
    }
)
class ECLintParser(ParserBase):
    """Parse eclint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            for line in output.split("\n"):
                try:
                    if "❌" not in line:
                        continue

                    parts = line.split("❌")
                    line_no = int(parts[0].split(":")[0].strip())
                    msg = parts[1].strip()
                    messages.add((file_path, line_no, msg))
                except (ValueError, IndexError, TypeError):
                    print("Invalid message: {0}".format(line))
        return messages
