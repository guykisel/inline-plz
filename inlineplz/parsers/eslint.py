# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class ESLintParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split('\n'):
            try:
                parts = line.split(':')
                if line.strip() and parts:
                    path = parts[0].strip()
                    line = int(parts[1].strip())
                    msgbody = ':'.join(parts[3:]).strip()
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                print('Invalid message: {0}'.format(line))
        return messages
