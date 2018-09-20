# -*- coding: utf-8 -*-

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="megacheck",
    install=[["go", "get", "-u", "honnef.co/go/tools/cmd/megacheck"]],
    help_cmd=["megacheck", "--help"],
    run=["megacheck", "-f", "json", "./..."],
    rundefault=["megacheck", "-f", "json", "./..."],
    dotfiles=[],
    language="go",
    autorun=False,
    run_per_file=False,
)
class MegacheckParser(ParserBase):
    """Parse json megacheck output."""

    def parse(self, lint_data):
        messages = set()
        msgdata = ""
        for line in lint_data.split("\n"):
            try:
                msgdata = json.loads(line)
                path = msgdata["location"]["file"]
                line = msgdata["location"]["line"]
                msgbody = msgdata["message"]
                messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, msgdata))
        return messages
