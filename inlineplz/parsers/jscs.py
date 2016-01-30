# -*- coding: utf-8 -*-
from __future__ import absolute_import

import json

from inlineplz.parsers.base import ParserBase
from inlineplz.message import Message


class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = []
        return messages
