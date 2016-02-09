# -*- coding: utf-8 -*-
from __future__ import absolute_import

import github3
import unidiff

from inlineplz.interfaces.base import InterfaceBase
from inlineplz.util import git


class GitHubInterface(InterfaceBase):
    def __init__(self, owner, repo, pr, token, url=None):
        self.github = None
        # TODO: support non-PR runs
        try:
            pr = int(pr)
        except ValueError:
            return
        if not url:
            self.github = github3.GitHub(token=token)
        else:
            self.github = github3.GitHubEnterprise(url, token=token)
        self.pull_request = self.github.pull_request(owner, repo, pr)
        # github3 has naming/compatibility issues
        try:
            self.commits = [c for c in self.pull_request.commits()]
        except (AttributeError, TypeError):
            self.commits = [c for c in self.pull_request.iter_commits()]
        self.last_sha = self.commits[-1].sha
        self.first_sha = self.commits[0].sha
        self.parent_sha = git.parent_sha(self.first_sha)
        self.diff = git.diff(self.parent_sha, self.last_sha)

    def post_messages(self, messages, max_comments):
        # TODO: support non-PR runs
        if not self.github:
            return
        messages_to_post = 0
        messages_posted = 0
        for msg in messages:
            if not msg.comments:
                continue
            msg_position = self.position(msg)
            if msg_position:
                messages_to_post += 1
                if not self.is_duplicate(msg, msg_position):
                    self.pull_request.create_review_comment(
                        self.format_message(msg),
                        self.last_sha,
                        msg.path,
                        msg_position
                    )
                    messages_posted += 1
                    if max_comments >= 0 and messages_posted > max_comments:
                        break
        return messages_to_post

    def is_duplicate(self, message, position):
        for comment in self.pull_request.review_comments():
            if (comment.position == position and
                    comment.path == message.path and
                    comment.body.strip() == self.format_message(message).strip()):
                return True
        return False

    @staticmethod
    def format_message(message):
        if not message.comments:
            return ''
        if len(message.comments) > 1:
            return (
                '```\n' +
                '\n'.join(sorted(list(message.comments))) +
                '\n```'
            )
        return '`{0}`'.format(list(message.comments)[0].strip())

    def position(self, message):
        """Calculate position within the PR, which is not the line number"""
        patch = unidiff.PatchSet(self.diff.split('\n'))
        for patched_file in patch:
            target = patched_file.target_file.lstrip('b/')
            if target == message.path:
                offset = 1
                for hunk_no, hunk in enumerate(patched_file):
                    for position, hunk_line in enumerate(hunk):
                        if '+' not in hunk_line.line_type:
                            continue
                        if hunk_line.target_line_no == message.line_number:
                            return position + offset
                    offset += len(hunk) + 1
