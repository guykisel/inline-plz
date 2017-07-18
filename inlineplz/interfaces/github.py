# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random
import time

import github3
import unidiff

from inlineplz.interfaces.base import InterfaceBase
from inlineplz.util import git, system


class GitHubInterface(InterfaceBase):
    def __init__(self, owner, repo, pr, token, url=None):
        self.github = None
        # TODO: support non-PR runs
        try:
            pr = int(pr)
        except (ValueError, TypeError):
            return
        if not url or url == 'https://github.com':
            self.github = github3.GitHub(token=token)
        else:
            self.github = github3.GitHubEnterprise(url, token=token)
        self.owner = owner
        self.repo = repo
        self.pr = pr
        self.pull_request = self.github.pull_request(owner, repo, pr)
        self.commits = self.pr_commits(self.pull_request)
        self.last_sha = self.commits[-1].sha
        self.first_sha = self.commits[0].sha
        self.parent_sha = git.parent_sha(self.first_sha)
        self.diff = git.diff(self.parent_sha, self.last_sha)

    @staticmethod
    def pr_commits(pull_request):
        # github3 has naming/compatibility issues
        try:
            return [c for c in pull_request.commits()]
        except (AttributeError, TypeError):
            return [c for c in pull_request.iter_commits()]

    def out_of_date(self):
        """Check if our local latest sha matches the remote latest sha"""
        pull_request = self.github.pull_request(self.owner, self.repo, self.pr)
        return self.last_sha != self.pr_commits(pull_request)[-1].sha

    def post_messages(self, messages, max_comments):
        # TODO: support non-PR runs
        if not self.github:
            return
        messages_to_post = 0
        messages_posted = 0
        paths = dict()

        # randomize message order to more evenly distribute messages across different files
        messages = list(messages)
        random.shuffle(messages)
        if self.out_of_date():
            return messages_to_post
        start = time.time()
        for msg in messages:
            if system.should_stop() or (time.time() - start > 10 and self.out_of_date()):
                return messages_to_post
            if not msg.comments:
                continue
            msg_position = self.position(msg)
            if msg_position:
                messages_to_post += 1
                if not self.is_duplicate(msg, msg_position):
                    # skip this message if we already have too many comments on this file
                    # max comments / 5 is an arbitrary number i totally made up. should maybe be configurable.
                    if paths.setdefault(msg.path, 0) > max_comments // 5:
                        continue
                    try:
                        self.pull_request.create_review_comment(
                            self.format_message(msg),
                            self.last_sha,
                            msg.path,
                            msg_position
                        )
                    except github3.GitHubError:
                        pass
                    paths[msg.path] += 1
                    messages_posted += 1
                    if max_comments >= 0 and messages_posted > max_comments:
                        break
        print('{} messages posted to Github.'.format(messages_to_post))
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
        if not message.line_number:
            message.line_number = 1
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
