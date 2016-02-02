# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from inlineplz.env.base import EnvBase


# https://wiki.jenkins-ci.org/display/JENKINS/Building+a+software+project#Buildingasoftwareproject-JenkinsSetEnvironmentVariables


class Jenkins(EnvBase):
    def __init__(self):
        if os.environ.get('ghprbActualCommit'):
            self.pull_request = os.environ.get('ghprbPullId')
            self.owner = os.environ.get('GITHUB_REPO_OWNER')
            self.repo = os.environ.get('GITHUB_REPO_NAME')
            self.commit = os.environ.get('ghprbActualCommit')
            self.interface = 'github'
            self.token = os.environ.get('GITHUB_TOKEN')
