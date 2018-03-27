# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class MegacheckParser(ParserBase):
    """Parse json megacheck output."""

    def parse(self, lint_data):
        messages = set()
        msgdata = ''
        for line in lint_data.split('\n'):
            try:
                msgdata = json.loads(line)
                path = msgdata['location']['file']
                line = msgdata['location']['line']
                msgbody = msgdata['message']
                messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print('Invalid message: {0}'.format(msgdata))
        return messages
