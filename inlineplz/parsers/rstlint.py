# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class RSTLintParser(ParserBase):
    """Parse json rst-lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                for msgdata in json.loads(output):
                    try:
                        path = file_path
                        line = msgdata['line']
                        msgbody = msgdata['message']
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print('Invalid message: {0}'.format(msgdata))
            except json.error.Error:
                print('Invalid message: {0}'.format(output))
        return messages
