# -*- coding: utf-8 -*-
from __future__ import absolute_import

import stashy
import unidiff

from inlineplz.interfaces.base import InterfaceBase
from inlineplz.util import git


class StashInterface(InterfaceBase):
    def __init__(self, project, repo, pr, username, password, url=None):
        # TODO: support non-PR runs
        try:
            pr = int(pr)
        except ValueError:
            return
        if not url:
            return
        else:
            self.stash = stashy.connect(url, username=username, password=password, verify=False)
        self.pull_request = self.stash.projects[project].repos[repo].pull_requests[pr]
        self.commits = [c for c in self.pull_request.commits()]
        self.last_sha = self.commits[0]['id']
        self.first_sha = self.commits[-1]['id']
        self.parent_sha = self.commits[-1]['parents'][0]['id']
        self.diff = git.diff(self.parent_sha, self.last_sha)

    def post_messages(self, messages, max_comments):
        # TODO: support non-PR runs
        if not self.stash:
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
                    self.pull_request.comment(
                        self.format_message(msg),
                        srcPath=msg.path,
                        fileLine=msg_position,
                        lineType='ADDED',
                        fileType='TO'
                    )
                    messages_posted += 1
                    if max_comments >= 0 and messages_posted > max_comments:
                        break
        return messages_to_post

    def is_duplicate(self, message, position):
        for comment in self.pull_request.comments(message.path):
            if ('anchor' in comment and
                    'line' in comment['anchor'] and
                    comment['anchor']['line'] == position and
                    comment['text'].strip() == self.format_message(message).strip()):
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
        """
        Determine where the comment should go

        Skips messages outside of the scope of changes we're looking at
        """
        patch = unidiff.PatchSet(self.diff.split('\n'))
        for patched_file in patch:
            target = patched_file.target_file.lstrip('b/')
            if target == message.path:
                for hunk_no, hunk in enumerate(patched_file):
                    for position, hunk_line in enumerate(hunk):
                        if '+' not in hunk_line.line_type:
                            continue
                        if hunk_line.target_line_no == message.line_number:
                            return hunk_line.target_line_no
