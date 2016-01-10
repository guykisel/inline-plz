# -*- coding: utf-8 -*-
from __future__ import absolute_import

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class ProspectorParser(ParserBase):
    """Parse default prospector output."""

    def parse(self, lint_data):
        messages = []
        current_filename = ''
        current_line = ''
        current_message_content = ''

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
                if current_message_content:
                    messages.append(Message(
                        current_filename,
                        current_line,
                        current_message_content
                    ))
                current_filename = line.strip()
                current_line = ''
                current_message_content = ''
                continue
            # new line number
            elif not line.startswith('    '):
                if current_message_content:
                    messages.append(Message(
                        current_filename,
                        current_line,
                        current_message_content
                    ))
                current_line = int(line.replace('  Line: ', '').strip())
                current_message_content = ''
                continue
            # new content
            current_message_content += line.lstrip()

        return messages
