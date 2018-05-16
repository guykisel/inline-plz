# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class ShellcheckParser(ParserBase):
    """Parse json shellcheck output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            if file_path.strip() and output.strip():
                filedata = json.loads(output)
                if filedata:
                    for msgdata in filedata:
                        try:
                            path = file_path
                            line = msgdata['line']
                            msgbody = msgdata['message']
                            messages.add((path, line, msgbody))
                        except (ValueError, KeyError, TypeError):
                            print('Invalid message: {0}'.format(msgdata))
        return messages
