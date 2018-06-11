# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class ECLintParser(ParserBase):
    """Parse eclint output."""

    def parse(self, lint_data):
        messages = set()
        path = ''
        for line in lint_data.split('\n'):
            try:
                if line.lstrip() != line:
                    path = line.strip()
                    continue
                parts = line.split('❌')
                line_no = int(parts[0].split(':').strip()[0])
                msg = parts[1].strip()
                messages.add((path, line_no, msg))
            except (ValueError, IndexError, TypeError):
                print('Invalid message: {0}'.format(line))
        return messages
