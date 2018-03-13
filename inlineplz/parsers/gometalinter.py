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
                path = msgdata['path']
                line = msgdata['line']
                msgbody = msgdata['linter'] + ': ' + msgdata['message']
                messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print('Invalid message: {0}'.format(msgdata))
        return messages
