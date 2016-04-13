# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

class ParserBase(object):
    """Abstract base class for parsers"""

    def parse(self, lint_data):
        """
        Parse linter output and return a list of messages.
        :param str lint_data: linter output in the form of a string
        :return: a list of Messages
        :rtype: list
        """
        raise NotImplementedError()
