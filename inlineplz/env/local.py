# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess

from inlineplz.env.base import EnvBase
import inlineplz.util.git as git


class Local(EnvBase):
    def __init__(self):
        if subprocess.check_call(['git status']):
            self.commit = git.current_sha()
