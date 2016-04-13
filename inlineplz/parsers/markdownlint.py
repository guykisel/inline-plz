# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class MarkdownLintParser(ParserBase):
    """Parse markdownlint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split('\n'):
            try:
                parts = line.split(':')
                if line.strip() and parts:
                    path = parts[0]
                    line = int(parts[1])
                    msgbody = parts[2].strip()
                    messages.add((path, line, msgbody))
            except ValueError:
                pass
        return messages
