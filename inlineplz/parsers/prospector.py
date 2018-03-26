# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import traceback

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class ProspectorParser(ParserBase):
    """Parse json prospector output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for msgdata in json.loads(lint_data).get('messages'):
                try:
                    path = msgdata['location']['path']
                    line = msgdata['location']['line']
                    msgbody = '{0}: {1} ({2})'.format(
                        msgdata['source'],
                        msgdata['message'],
                        msgdata['code']
                    )
                    messages.add((path, line, msgbody))
                except (ValueError, KeyError):
                    print('Invalid message: {0}'.format(msgdata))
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
