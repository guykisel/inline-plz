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
    def __init__(self, owner, repo, pr=None, branch=None, token=None, url=None, commit=None, ignore_paths=None):
        """
        GitHubInterface lets us post messages to GitHub.

        owner and repo are the repository owner/organization and repo name respectively.

        pr is the ID number of the pull request. branch is the branch name. either pr OR branch
        must be populated.

        token is your GitHub API token.

        url is the base URL of your GitHub instance, such as https://github.com

        commit is the commit hash we're running against

        ignore_paths are paths to ignore comments from
        """
        self.github = None
        self.ignore_paths = set(ignore_paths or [])
        if not url or url == 'https://github.com':
            self.github = github3.GitHub(token=token)
        else:
            self.github = github3.GitHubEnterprise(url, token=token)
        self.owner = owner
        self.repo = repo

        github_repo = self.github.repository(self.owner, self.repo)
        all_commits = self.repo_commits(github_repo)
        self.master_sha = all_commits[0].sha
        print('Master SHA: {0}'.format(self.master_sha))

        print('Branch: {0}'.format(branch))
        if branch and not pr:
            github_repo = self.github.repository(self.owner, self.repo)
            for pull_request in github_repo.iter_pulls():
                if pull_request.to_json()['head']['ref'] == branch:
                    pr = pull_request.to_json()['number']
                    break

        # TODO: support non-PR runs
        try:
            pr = int(pr)
        except (ValueError, TypeError):
            print('{0} is not a valid pull request ID'.format(pr))
            self.github = None
            return
        print('PR ID: {0}'.format(pr))
        self.pr = pr
        self.pull_request = self.github.pull_request(owner, repo, pr)
        self.commits = self.pr_commits(self.pull_request)
        self.last_sha = commit or git.current_sha()
        print('Last SHA: {0}'.format(self.last_sha))
        self.first_sha = self.commits[0].sha
        self.diff = git.diff(self.master_sha, self.last_sha)
        self.patch = unidiff.PatchSet(self.diff.split('\n'))
        self.review_comments = list(self.pull_request.review_comments())
        self.last_update = time.time()

    @staticmethod
    def pr_commits(pull_request):
        # github3 has naming/compatibility issues
        try:
            return [c for c in pull_request.commits()]
        except (AttributeError, TypeError):
            return [c for c in pull_request.iter_commits()]

    @staticmethod
    def repo_commits(repo):
        # github3 has naming/compatibility issues
        try:
            return [c for c in repo.commits()]
        except (AttributeError, TypeError):
            return [c for c in repo.iter_commits()]

    def out_of_date(self):
        """Check if our local latest sha matches the remote latest sha"""
        pull_request = self.github.pull_request(self.owner, self.repo, self.pr)
        latest_remote_sha = self.pr_commits(pull_request)[-1].sha
        return self.last_sha != latest_remote_sha

    def post_messages(self, messages, max_comments):
        # TODO: support non-PR runs
        if not self.github:
            print('Github connection is invalid.')
            return
        messages_to_post = 0
        messages_posted = 0
        paths = dict()

        # randomize message order to more evenly distribute messages across different files
        messages = list(messages)
        random.shuffle(messages)
        if self.out_of_date():
            print('This run is out of date because the PR has been updated.')
            messages = []
        start = time.time()
        print("Considering {} messages for posting.".format(len(messages)))
        for msg in messages:
            print('\nTrying to post a review comment.')
            print('{0}'.format(msg))
            if system.should_stop() or (time.time() - start > 10 and self.out_of_date()):
                print('Stopping early.')
                break
            if not msg.comments:
                print("Skipping since there is no comment to post.")
                continue
            msg_position = self.position(msg)
            if not msg_position:
                print("Skipping since the comment is not part of this PR.")
                continue
            messages_to_post += 1
            if self.is_duplicate(msg, msg_position):
                print("Skipping since this comment already exists.")
                continue
            # skip this message if we already have too many comments on this file
            # max comments / 5 is an arbitrary number i totally made up. should maybe be configurable.
            if paths.setdefault(msg.path, 0) > max(max_comments // 5, 5):
                print("Skipping since we reached the maximum number of comments for this file.")
                continue
            if msg.path.split('/')[0] in self.ignore_paths:
                print("Skipping since the comment is on an ignored path.")
                continue
            try:
                self.pull_request.create_review_comment(
                    self.format_message(msg),
                    self.last_sha,
                    msg.path,
                    msg_position
                )
            except github3.GitHubError as err:
                print("Posting failed: {}".format(err))
                continue
            print("Comment posted successfully.")
            paths[msg.path] += 1
            messages_posted += 1
            if max_comments and messages_posted > max_comments:
                break
        print('\n{} messages posted to Github.'.format(messages_posted))
        return messages_to_post

    def is_duplicate(self, message, position):
        # update our list of review comments about once a second
        # to reduce dupes without hitting the API too hard
        if time.time() - self.last_update > 1:
            self.review_comments = list(self.pull_request.review_comments())
            self.last_update = time.time()
        for comment in self.review_comments:
            if (comment.original_position == position and
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
        for patched_file in self.patch:
            target = patched_file.target_file.lstrip('b/')
            if target == message.path:
                offset = 1
                for hunk in patched_file:
                    for position, hunk_line in enumerate(hunk):
                        if hunk_line.target_line_no == message.line_number:
                            return position + offset
                    offset += len(hunk) + 1
