# -*- coding: utf-8 -*-

import os

from ..env.base import EnvBase

try:
    import urllib.parse as urlparse
except ImportError:
    # pylint: disable=F0401
    import urlparse


# https://wiki.jenkins-ci.org/display/JENKINS/Building+a+software+project#Buildingasoftwareproject-JenkinsSetEnvironmentVariables


class Jenkins(EnvBase):
    def __init__(self):
        if os.environ.get("ghprbPullId") or os.environ.get("ghprbActualCommit"):
            self.pull_request = os.environ.get("ghprbPullId")
            self.owner = (
                os.environ.get("GITHUB_REPO_OWNER")
                or os.environ.get("ghprbPullLink").split("/")[-4]
            )
            self.repo = (
                os.environ.get("GITHUB_REPO_NAME")
                or os.environ.get("ghprbPullLink").split("/")[-3]
            )
            self.commit = os.environ.get("ghprbActualCommit")
            self.interface = "github"
            self.token = os.environ.get("GITHUB_TOKEN")
            spliturl = urlparse.urlsplit(os.environ.get("ghprbPullLink"))
            if spliturl.netloc != "github.com":
                self.url = "{0}://{1}".format(spliturl.scheme, spliturl.netloc)
