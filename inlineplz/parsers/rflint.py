# -*- coding: utf-8 -*-
from __future__ import absolute_import

from inlineplz.parsers.base import ParserBase


class RobotFrameworkLintParser(ParserBase):
    """Parse rflint output."""

    def parse(self, lint_data):
        messages = set()
        current_file = None
        for line in lint_data.split('\n'):
            try:
                if line.startswith('+'):
                    current_file = line.split(' ')[1]
                    continue
                else:
                    _, position, message = line.split(':')
                    line_number, _ = position.split(',')
                    messages.add((current_file, int(line_number), message.strip()))
            except ValueError:
                pass

        return messages
