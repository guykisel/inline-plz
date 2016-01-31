# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class ProspectorParser(ParserBase):
    """Parse json prospector output."""

    def parse(self, lint_data):
        messages = []
        for msgdata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ).get('messages'):
            msg = Message(
                msgdata['location']['path'],
                msgdata['location']['line']
            )
            msgbody = '{0}: {1} ({2})'.format(
                msgdata['source'],
                msgdata['message'],
                msgdata['code']
            )
            msg.comments.append(msgbody)
            messages.append(msg)
        return messages
