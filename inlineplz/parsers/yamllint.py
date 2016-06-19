# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class YAMLLintParser(ParserBase):
    """Parse yaml-lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                if file_path.strip() and output.strip():
                    path = file_path
                    line = int(output.split('at line')[1].split()[0].strip())
                    msgbody = output
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                pass
        return messages
