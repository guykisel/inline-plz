# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class CodenarcParser(ParserBase):
    """Parse Codenarc output."""

    def parse(self, lint_data):
        messages = set()
        path = ''
        for line in lint_data.split('\n'):
            try:
                line = line.strip()
                if line.startswith('File:'):
                    path = line.split('File:')[-1].strip()
                    continue
                if line.startswith('Violation:'):
                    parts = line.split()
                    line_no = int(parts[3].split('=')[-1])
                    msg = ' '.join(parts[4:-1]).split('Src=')[0]
                    messages.add((path, line_no, msg))
            except (ValueError, IndexError, TypeError):
                print('Invalid message: {0}'.format(line))
        return messages
