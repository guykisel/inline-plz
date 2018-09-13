# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import re

from inlineplz.parsers.base import ParserBase
import dirtyjson as json


class TFLintParser(ParserBase):
    """Parse tflint output."""

    def parse(self, lint_data):
        messages = set()

        for error_stanza in json.loads(lint_data):
            messages.add((
                error_stanza.get('file', None),
                error_stanza.get('line', None),
                error_stanza.get('message', None),
            ))

        return messages
