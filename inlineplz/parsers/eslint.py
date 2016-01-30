# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json
import os.path

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class ESLintParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = []
        for filedata in json.loads(lint_data):
            if filedata.get('messages'):
                for msgdata in filedata['messages']:
                    msg = Message(
                        filedata.get('filePath'),
                        msgdata.get('line')
                    )
                    msg.comments.append(msgdata.get('message'))
                    messages.append(msg)
        return messages
