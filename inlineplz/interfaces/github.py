# -*- coding: utf-8 -*-
from __future__ import absolute_import

import subprocess

import github3
import unidiff

from .base import InterfaceBase


class GitHubInterface(InterfaceBase):
    def __init__(self, owner, repo, pr, token, url=None):
        if not url:
            self.gh = github3.GitHub(token=token)
        else:
            self.gh = github3.GitHubEnterprise(url, token=token)
        self.pull_request = self.gh.pull_request(owner, repo, pr)
        self.sha = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD']
        ).strip().decode('utf-8')
        self.diff = self.pull_request.diff()

    def post_messages(self, messages):
        for msg in messages:
            if not msg.content:
                continue
            msg_position = self.position(msg)
            if msg_position:
                # check for dupes so we don't spam the PR
                duplicate = False
                for comment in self.pull_request.review_comments():
                    if (comment.position == msg_position and
                            comment.path == msg.path and
                            comment.body.strip() == msg.content.strip()):
                        duplicate = True
                        break
                    continue
                if not duplicate:
                    self.pull_request.create_review_comment(
                        msg.content,
                        self.sha,
                        msg.path,
                        msg_position
                    )

    def position(self, message):
        """Calculate position within the PR, which is not the line number"""
        patch = unidiff.PatchSet(self.diff.decode('utf-8').split('\n'))
        for patched_file in patch:
            if patched_file.target_file == 'b/' + message.path:
                offset = 1
                for hunk_no, hunk in enumerate(patched_file):
                    for position, hunk_line in enumerate(hunk):
                        if '+' not in hunk_line.line_type:
                            continue
                        if hunk_line.target_line_no == message.line_number:
                            return position + offset
                    offset += len(hunk) + 1
