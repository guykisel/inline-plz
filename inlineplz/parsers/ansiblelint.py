# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.parsers.base import ParserBase


class AnsibleLintParser(ParserBase):
    """Parse Ansible Lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            if file_path.strip() and output.strip():
                for line in output.split('\n'):
                    try:
                        if line.strip():
                            parts = line.split(':')
                            path = parts[0].strip()
                            line_no = int(parts[1].strip())
                            msgbody = parts[2].strip()
                            messages.add((path, line_no, msgbody))
                    except (ValueError, IndexError, TypeError):
                        print('Invalid message: {0}'.format(line))
        return messages
