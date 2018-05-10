# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


from inlineplz.parsers.base import ParserBase


class SpotbugsMavenParser(ParserBase):
    """Parse Spotbugs Maven output."""

    def parse(self, lint_data):
        messages = set()
        project = ''
        for line in lint_data.split('\n'):
            try:
                if '@' in line:
                    project = line.split('@')[1].strip().split()[0]
                    continue
                if '[line' in line:
                    msgbody = line
                    line_number = int(line.split('[line ')[1].split(']')[0])
                    path_parts = line.split('[')[-2].split(']')[0].split('$')[0].split('.')
                    path_parts[-1] = path_parts[-1] + '.java'
                    path_base = [project, 'src', 'main', 'java']
                    path_base.extend(path_parts)
                    path = '/'.join(path_base)
                    messages.add((path, line_number, msgbody))
            except (ValueError, IndexError):
                print('Invalid message: {0}'.format(line))
        return messages
