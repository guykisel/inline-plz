# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class ECLintParser(ParserBase):
    """Parse eclint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            for line in output.split('\n'):
                try:
                    if '❌' not in line:
                        continue
                    parts = line.split('❌')
                    line_no = int(parts[0].split(':')[0].strip())
                    msg = parts[1].strip()
                    messages.add((file_path, line_no, msg))
                except (ValueError, IndexError, TypeError):
                    print('Invalid message: {0}'.format(line))
        return messages
