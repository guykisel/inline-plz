# -*- coding: utf-8 -*-
from __future__ import absolute_import


class InterfaceBase(object):
    """Abstract base class for review interfaces"""

    def post_messages(self, messages):
        """

        :param messages:
        :return:
        """
        raise NotImplementedError()
