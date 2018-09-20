# -*- coding: utf-8 -*-
import sys
import traceback

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="detect-secrets",
    install=[[sys.executable, "-m", "pip", "install", "-U", "detect-secrets"]],
    help_cmd=["detect-secrets", "-h"],
    run=["detect-secrets", "scan", "--all-files"],
    rundefault=["detect-secrets", "scan", "--all-files"],
    dotfiles=[],
    language="all",
    autorun=True,
    run_per_file=False,
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
                        print(
                            "({0}) Invalid message: {1}".format(
                                type(self).__name__, msgdata
                            )
                        )
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
