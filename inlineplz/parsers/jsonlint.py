# -*- coding: utf-8 -*-
from __future__ import absolute_import

from inlineplz.parsers.base import ParserBase


class JSONLintParser(ParserBase):
    """Parse jsonlint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            path = file_path
            line = int(output.split(':')[1].split()[1].strip(', '))
            msgbody = output
            messages.add((path, line, msgbody))
        return messages
