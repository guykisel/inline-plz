# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xmltodict

from inlineplz.parsers.base import ParserBase


class JSHintParser(ParserBase):
    """Parse json jshint output."""

    def parse(self, lint_data):
        messages = set()
        obj = xmltodict.parse(lint_data)
        for filedata in obj['checkstyle']['file']:
            for errordata in filedata['error']:
                try:
                    path = filedata['@name']
                    line = int(errordata['@line'])
                    msgbody = errordata['@message']
                    messages.add((path, line, msgbody))
                except (AttributeError, TypeError):
                    pass
        return messages
