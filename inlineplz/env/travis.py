# -*- coding: utf-8 -*-

import os

from ..env.base import EnvBase

# https://docs.travis-ci.com/user/environment-variables/#Default-Environment-Variables


class Travis(EnvBase):
    def __init__(self):
        self.pull_request = os.environ.get("TRAVIS_PULL_REQUEST")
        self.branch = os.environ.get("TRAVIS_BRANCH")
        self.repo_slug = os.environ.get("TRAVIS_REPO_SLUG")
        self.commit = os.environ.get("TRAVIS_PULL_REQUEST_SHA")
        self.commit_range = os.environ.get("TRAVIS_COMMIT_RANGE")
        self.interface = "github"
        self.token = os.environ.get("GITHUB_TOKEN")
