# -*- coding: utf-8 -*-
from __future__ import absolute_import

from collections import OrderedDict
import json

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class ESLintParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = []
        for filedata in json.loads(
            lint_data,
            object_pairs_hook=OrderedDict
        ):
            if filedata.get('messages'):
                for msgdata in filedata['messages']:
                    msg = Message(
                        filedata.get('filePath'),
                        msgdata.get('line')
                    )
                    msg.append(msgdata.get('message'))
                    messages.append(msg)
        return messages
