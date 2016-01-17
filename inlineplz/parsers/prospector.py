# -*- coding: utf-8 -*-
from __future__ import absolute_import

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class ProspectorParser(ParserBase):
    """Parse default prospector output."""

    def parse(self, lint_data):
        messages = []
        current_message = None
        current_filename = ''
        current_line = ''

        messages_found = False

        for line in lint_data.split('\n'):
            # check for message block
            if not line.strip():
                continue
            if not messages_found:
                if line.strip() == 'Messages':
                    messages_found = True
                continue
            # check for end of message block
            elif line.strip() == 'Check Information':
                break
            # new filename
            if not line.startswith(' '):
                current_filename = line.strip()
                continue
            # new line number
            elif not line.startswith('    '):
                current_line = int(line.replace('  Line: ', '').strip())
                current_message = Message(current_filename, current_line)
                messages.append(current_message)
                continue
            # new content
            current_message.comments.append(line.lstrip())

        return messages
