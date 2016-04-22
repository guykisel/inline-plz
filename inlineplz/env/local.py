# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os

import inlineplz.util.git as git
from inlineplz.env.base import EnvBase


class Local(EnvBase):
    def __init__(self):
        if os.path.exists('.git'):
            self.commit = git.current_sha()
