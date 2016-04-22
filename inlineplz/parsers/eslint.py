# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json
from collections import OrderedDict

from inlineplz.parsers.base import ParserBase


class ESLintParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for filedata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ):
            if filedata.get('messages'):
                for msgdata in filedata['messages']:
                    path = filedata['filePath']
                    line = msgdata['line']
                    msgbody = msgdata['message']
                    messages.add((path, line, msgbody))
        return messages
