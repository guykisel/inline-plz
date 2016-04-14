from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class GherkinLintParser(ParserBase):
    """Parse json gherkin-lint output."""

    def parse(self, lint_data):
        messages = set()
        for filedata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ):
            if filedata.get('errors'):
                path = filedata['filePath']
                for msgdata in filedata['errors']:
                    line = msgdata['line']
                    msgbody = msgdata['message']
                    messages.add((path, line, msgbody))
        return messages
