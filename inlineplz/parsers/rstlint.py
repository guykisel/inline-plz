# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class RSTLintParser(ParserBase):
    """Parse json rst-lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            for msgdata in json.loads(
                output,
                object_pairs_hook=OrderedDict
            ):
                path = file_path
                line = msgdata['line']
                msgbody = msgdata['message']
                messages.add((path, line, msgbody))
        return messages
