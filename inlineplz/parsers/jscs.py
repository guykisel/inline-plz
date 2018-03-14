# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = set()
        for filename, msgs in json.loads(lint_data).items():
            if msgs:
                for msgdata in msgs:
                    try:
                        path = filename
                        line = msgdata['line']
                        msgbody = msgdata['message']
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print('Invalid message: {0}'.format(msgdata))
        return messages
