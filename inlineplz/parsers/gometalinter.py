# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class GometalinterParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for msgdata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ):
            path = msgdata['path']
            line = msgdata['line']
            msgbody = msgdata['linter'] + ': ' + msgdata['message']
            messages.add((path, line, msgbody))
        return messages
