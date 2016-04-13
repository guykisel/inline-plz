# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os

from inlineplz.env.base import EnvBase


# https://docs.travis-ci.com/user/environment-variables/#Default-Environment-Variables


class Travis(EnvBase):
    def __init__(self):
        self.pull_request = os.environ.get('TRAVIS_PULL_REQUEST')
        self.repo_slug = os.environ.get('TRAVIS_REPO_SLUG')
        self.commit = os.environ.get('TRAVIS_COMMIT')
        self.commit_range = os.environ.get('TRAVIS_COMMIT_RANGE')
        self.interface = 'github'
        self.token = os.environ.get('GITHUB_TOKEN')
