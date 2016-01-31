# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = []
        for filename, msgs in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ).items():
            if msgs:
                for m in msgs:
                    msg = Message(
                        filename,
                        m.get('line')
                    )
                    msg.comments.append(m.get('message'))
                    messages.append(msg)
        return messages
