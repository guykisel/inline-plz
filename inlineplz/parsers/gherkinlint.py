from __future__ import absolute_import
from __future__ import unicode_literals

import traceback

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class GherkinLintParser(ParserBase):
    """Parse json gherkin-lint output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for filedata in json.loads(lint_data):
                if filedata.get('errors') and filedata.get('filePath'):
                    path = filedata['filePath']
                    for msgdata in filedata['errors']:
                        try:
                            line = msgdata['line']
                            msgbody = msgdata['message']
                            messages.add((path, line, msgbody))
                        except (ValueError, KeyError):
                            print('Invalid message: {0}'.format(msgdata))
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
