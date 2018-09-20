# -*- coding: utf-8 -*-

import os

from ..env.base import EnvBase
from ..util import git


class Local(EnvBase):
    def __init__(self):
        if os.path.exists(".git"):
            self.interface = "github"
            self.commit = git.current_sha()
            self.branch = git.current_branch()
            self.url = git.url()
