# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

import github3
import unidiff

from inlineplz.interfaces.base import InterfaceBase
from inlineplz.util import git


class GitHubInterface(InterfaceBase):
    def __init__(self, owner, repo, pr, token, url=None):
        if not url:
            self.gh = github3.GitHub(token=token)
        else:
            self.gh = github3.GitHubEnterprise(url, token=token)
        self.pull_request = self.gh.pull_request(owner, repo, pr)
        self.commits = [c for c in self.pull_request.commits()]
        self.last_sha = self.commits[-1].sha
        self.first_sha = self.commits[0].sha
        self.parent_sha = git.parent_sha(self.first_sha)
        self.diff = git.diff(self.parent_sha, self.last_sha)

    def post_messages(self, messages):
        for msg in messages:
            if not msg.content:
                continue
            msg_position = self.position(msg)
            if msg_position:
                if not self.is_duplicate(msg, msg_position):
                    self.pull_request.create_review_comment(
                        msg.content,
                        self.last_sha,
                        # need to make paths unixy to make github happy
                        msg.path.replace('\\', '/'),
                        msg_position
                    )

    def is_duplicate(self, message, position):
        for comment in self.pull_request.review_comments():
            if (comment.position == position and
                    comment.path == message.path and
                    comment.body.strip() == message.content.strip()):
                return True
        return False

    def position(self, message):
        """Calculate position within the PR, which is not the line number"""
        patch = unidiff.PatchSet(self.diff.split('\n'))
        for patched_file in patch:
            if os.path.normpath(patched_file.target_file) == os.path.normpath('b/' + message.path):
                offset = 1
                for hunk_no, hunk in enumerate(patched_file):
                    for position, hunk_line in enumerate(hunk):
                        if '+' not in hunk_line.line_type:
                            continue
                        if hunk_line.target_line_no == message.line_number:
                            return position + offset
                    offset += len(hunk) + 1
