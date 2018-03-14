# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class RobotFrameworkLintParser(ParserBase):
    """Parse rflint output."""

    def parse(self, lint_data):
        messages = set()
        current_file = None
        for _, output in lint_data:
            for line in output.split('\n'):
                try:
                    if not line.strip():
                        continue
                    if line.startswith('+'):
                        current_file = line[2:]
                        continue
                    else:
                        _, position, message = line.split(':')
                        line_number, _ = position.split(',')
                        messages.add((current_file.strip(), int(line_number), message.strip()))
                except (ValueError, IndexError):
                    print('Invalid message: {0}'.format(line))
        return messages
