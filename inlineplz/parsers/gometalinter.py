# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class GometalinterParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for msgdata in json.loads(lint_data):
            try:
                path = msgdata["path"]
                line = msgdata["line"]
                msgbody = msgdata["linter"] + ": " + msgdata["message"]
                messages.add((path, line, msgbody))
            except (ValueError, KeyError, TypeError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, msgdata))
        return messages
