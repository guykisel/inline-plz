# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class JSONLintParser(ParserBase):
    """Parse jsonlint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                if file_path.strip() and output.strip():
                    path = file_path
                    line = int(output.split(':')[1].split()[1].strip(', '))
                    msgbody = output
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                print('Invalid message: {0}'.format(output))
        return messages
