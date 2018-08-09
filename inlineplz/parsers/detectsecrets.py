# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import traceback

import dirtyjson as json

from inlineplz.parsers.base import ParserBase


class DetectSecretsParser(ParserBase):
    """Parse json detect-secrets output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for path, msgs in json.loads(lint_data).get("results").items():
                for msgdata in msgs:
                    try:
                        line = msgdata["line_number"]
                        msgbody = msgdata["type"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print("Invalid message: {0}".format(msgdata))
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
