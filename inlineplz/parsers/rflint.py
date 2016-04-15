# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class RobotFrameworkLintParser(ParserBase):
    """Parse rflint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            for line in output.split('\n'):
                try:
                    if line.startswith('+'):
                        continue
                    else:
                        _, position, message = line.split(':')
                        line_number, _ = position.split(',')
                        messages.add((file_path, int(line_number), message.strip()))
                except ValueError:
                    pass

        return messages
