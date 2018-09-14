# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import traceback
import sys
import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    {
        # TODO: switch this to installing from pypi once they release my fix from https://github.com/Yelp/detect-secrets/pull/69
        # "install": [[sys.executable, "-m", "pip", "install", "-U", "detect-secrets"]],
        "name": "detect-secrets",
        "install": [[sys.executable, "-m", "pip", "install", "-U", "detect-secrets"]],
        "help": ["detect-secrets", "-h"],
        "run": ["detect-secrets", "scan", "--all-files"],
        "rundefault": ["detect-secrets", "scan", "--all-files"],
        "dotfiles": [],
        "language": "all",
        "autorun": True,
        "run_per_file": False,
    }
)
class DetectSecretsParser(ParserBase):
    """Parse json detect-secrets output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for path, msgs in json.loads(lint_data).get("results").items():
                for msgdata in msgs:
                    try:
                        line = msgdata["line_number"]
                        msgbody = msgdata["type"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print("Invalid message: {0}".format(msgdata))
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
