# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class YAMLLintParser(ParserBase):
    """Parse yaml-lint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split('\n'):
            try:
                if line.strip():
                    parts = line.split(':')
                    path = parts[0].strip()
                    line = int(parts[1].strip())
                    msgbody = parts[3].strip()
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError, TypeError):
                print('Invalid message: {0}'.format(lint_data))
        return messages
