# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class DockerfileLintParser(ParserBase):
    """Parse json dockerfile_lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            if file_path.strip() and output.strip():
                filedata = json.loads(output)
                for msgtype in ['error', 'warn', 'info']:
                    if filedata[msgtype]['count']:
                        for msgdata in filedata[msgtype].get('data', []):
                            try:
                                path = file_path
                                line = msgdata.get('line', 1)
                                msgbody = msgdata['message']
                                description = msgdata.get('description')
                                if description and description != 'None':
                                    msgbody += ' ({0})'.format(description)
                                messages.add((path.strip(), line, msgbody.strip()))
                            except (ValueError, KeyError, TypeError):
                                print('Invalid message: {0}'.format(msgdata))
        return messages
