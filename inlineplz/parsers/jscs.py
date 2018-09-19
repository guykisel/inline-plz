# -*- coding: utf-8 -*-

import dirtyjson as json

from ..parsers.base import ParserBase


class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = set()
        for filename, msgs in json.loads(lint_data).items():
            if msgs:
                for msgdata in msgs:
                    try:
                        path = filename
                        line = msgdata["line"]
                        msgbody = msgdata["message"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print(
                            "({0}) Invalid message: {1}".format(
                                type(self).__name__, msgdata
                            )
                        )
        return messages
