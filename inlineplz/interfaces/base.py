# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals


class InterfaceBase(object):
    """Abstract base class for review interfaces"""

    def post_messages(self, messages, max_comments):
        """

        :param messages:
        :return:
        """
        raise NotImplementedError()
