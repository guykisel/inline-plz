# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class ProselintParser(ParserBase):
    """Parse proselint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            try:
                if file_path.strip() and output.strip():
                    for line in output.split('\n'):
                        parts = line.split(':')
                        line = int(parts[1].strip())
                        msgbody = ':'.join(parts[2:]).strip()
                        messages.add((file_path, line, msgbody))
            except (ValueError, IndexError):
                print('Invalid message: {0}'.format(output))
        return messages
