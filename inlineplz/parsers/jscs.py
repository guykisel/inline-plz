# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = set()
        for filename, msgs in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ).items():
            if msgs:
                for msgdata in msgs:
                    path = filename
                    line = msgdata['line']
                    msgbody = msgdata['message']
                    messages.add((path, line, msgbody))
        return messages
