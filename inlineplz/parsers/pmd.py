# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class PMDParser(ParserBase):
    """Parse PMD output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split("\n"):
            try:
                if line.strip():
                    parts = line.split(":")
                    path = parts[0].strip()
                    line_no = int(parts[1].strip())
                    msgbody = parts[2].strip()
                    messages.add((path, line_no, msgbody))
            except (ValueError, IndexError, TypeError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, line))
        return messages
