# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class InterfaceBase(object):
    """Abstract base class for review interfaces"""

    def start_review(self):
        raise NotImplementedError()

    def finish_review(self, success=True, error=False):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()

    def post_messages(self, messages, max_comments):
        """

        :param messages:
        :return:
        """
        raise NotImplementedError()
