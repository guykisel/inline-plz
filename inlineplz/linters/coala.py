# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    {
        "name": "coala",
        "install": [
            [sys.executable, "-m", "pip", "install", "-U", "coala-bears"]
        ],
        "help": ["coala", "-h"],
        "run": ["coala", "-C"],
        "rundefault": ["coala", "--json", "-c", "{config_dir}/.coafile"],
        "dotfiles": [".coafile"],
        "language": "all",
        "autorun": True,
        "run_per_file": False,
    }
)
class CoalaParser(ParserBase):
    """Parse json coala output."""

    def parse(self, output):
        messages = set()
        lint_data = [
            msg
            for category in json.loads(output).get("results", {}).values()
            for msg in category
        ]
        for msgdata in lint_data:
            try:
                msgbody = msgdata["message"]
                for line in msgdata.get("affected_code", []):
                    path = line.get("file")
                    line = line.get("start", {}).get("line")
                    messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print("Invalid message: {0}".format(msgdata))
        return messages
