# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase


class ProspectorParser(ParserBase):
    """Parse json prospector output."""

    def parse(self, lint_data):
        messages = set()
        for msgdata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ).get('messages'):
            path = msgdata['location']['path']
            line = msgdata['location']['line']
            msgbody = '{0}: {1} ({2})'.format(
                msgdata['source'],
                msgdata['message'],
                msgdata['code']
            )
            messages.add((path, line, msgbody))
        return messages
