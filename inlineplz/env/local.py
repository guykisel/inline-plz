# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from inlineplz.env.base import EnvBase
import inlineplz.util.git as git


class Local(EnvBase):
    def __init__(self):
        if os.path.exists('.git'):
            self.interface = 'github'
            self.commit = git.current_sha()
            self.branch = git.current_branch()
            self.url = git.url()
