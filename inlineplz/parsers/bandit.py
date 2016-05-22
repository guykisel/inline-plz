# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class BanditParser(ParserBase):
    """Parse json bandit output."""

    def parse(self, lint_data):
        messages = set()
        lint_data_lines = lint_data.split('\n')
        # bandit spits out some unwanted debug messages before the json
        for line in lint_data_lines[:]:
            if line.strip().startswith('[main]'):
                lint_data_lines.remove(line)
        lint_data_cleaned = '\n'.join(lint_data_lines).strip()
        for msgdata in json.loads(
            lint_data_cleaned,
            object_pairs_hook=OrderedDict
        ).get('results'):
            path = msgdata['filename']
            line = msgdata['line_number']
            msgbody = msgdata['issue_text']
            messages.add((path, line, msgbody))
        return messages
