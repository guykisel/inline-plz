# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xmltodict

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class JSHintParser(ParserBase):
    """Parse json jshint output."""

    def parse(self, lint_data):
        messages = []
        obj = xmltodict.parse(lint_data)
        for filedata in obj['checkstyle']['file']:
            for errordata in filedata['error']:
                try:
                    msg = Message(
                        filedata.get('@name'),
                        int(errordata.get('@line'))
                    )
                    msg.append(errordata.get('@message'))
                    messages.append(msg)
                except AttributeError:
                    pass
        return messages
