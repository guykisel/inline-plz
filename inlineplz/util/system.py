# -*- coding: utf-8 -*-

"""
System utilities
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import os


STOP_FILE_NAME = '.inlineplzstop'


def should_stop():
    return os.path.isfile(os.path.join(os.getcwd(), STOP_FILE_NAME))
