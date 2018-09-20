# -*- coding: utf-8 -*-

import random
import subprocess
import time
import traceback

import github3
import unidiff

from ..interfaces.base import InterfaceBase
from ..util import git, system


class GitHubInterface(InterfaceBase):
    def __init__(
        self,
        owner,
        repo,
        pr=None,
        branch=None,
        token=None,
        url=None,
        commit=None,
        ignore_paths=None,
        prefix=None,
    ):
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
        self.stopped_early = False
        self.prefix = prefix
        self.ignore_paths = set(ignore_paths or [])
        if not url or url == "https://github.com":
            self.github = github3.GitHub(token=token)
        else:
            self.github = github3.GitHubEnterprise(url, token=token)
        self.owner = owner
        self.repo = repo

        self.github_repo = self.github.repository(self.owner, self.repo)
        all_commits = self.repo_commits(self.github_repo)
        self.master_sha = all_commits[0].sha
        print("Master SHA: {0}".format(self.master_sha))

        print("Branch: {0}".format(branch))
        self.pull_request_number = None
        if branch and not pr:
            for github_repo in [self.github_repo, self.github_repo.parent]:
                if pr:
                    break

                if not github_repo:
                    continue

                try:
                    # github.py == 0.9.6
                    pulls = github_repo.iter_pulls()
                except AttributeError:
                    pulls = github_repo.pull_requests()

                for pull_request in pulls:
                    print(
                        "Branch: {} - Pull Request Head Ref: {}".format(
                            branch, pull_request.head.ref
                        )
                    )
                    if pull_request.head.ref == branch:
                        pr = pull_request.number
                        self.github_repo = github_repo
                        break

        self.owner = self.github_repo.owner
        self.repo = self.github_repo.name

        # TODO: support non-PR runs
        try:
            pr = int(pr)
        except (ValueError, TypeError):
            print("{0} is not a valid pull request ID".format(pr))
            self.github = None
            return

        print("PR ID: {0}".format(pr))
        self.pull_request_number = pr
        self.pull_request = self.github.pull_request(self.owner, self.repo, pr)
        self.target_sha = self.pull_request.base.sha
        self.target_branch = self.pull_request.base.label
        try:
            # github.py == 0.9.6
            try:
                git.fetch(self.pull_request.base.to_json()["repo"]["clone_url"])
            except subprocess.CalledProcessError:
                git.fetch(self.pull_request.base.to_json()["repo"]["ssh_url"])
        except AttributeError:
            # latest github.py
            try:
                git.fetch(self.pull_request.base.repository.as_dict()["clone_url"])
            except subprocess.CalledProcessError:
                git.fetch(self.pull_request.base.repository.as_dict()["ssh_url"])

        print("Target SHA: {0}".format(self.target_sha))
        print("Target Branch: {0}".format(self.target_branch))
        self.commits = self.pr_commits(self.pull_request)
        self.last_sha = commit or git.current_sha()
        print("Last SHA: {0}".format(self.last_sha))
        self.first_sha = self.commits[0].sha
        self.diff = git.diff(self.target_sha, self.last_sha)
        self.patch = unidiff.PatchSet(self.diff.split("\n"))
        self.review_comments = list(self.pull_request.review_comments())
        self.last_update = time.time()
        self.messages_in_files = dict()

    def is_valid(self):
        return self.pull_request_number is not None

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

    def start_review(self):
        """Mark our review as started."""
        self.github_repo.create_status(
            state="pending",
            description="Static analysis in progress.",
            context="inline-plz",
            sha=self.last_sha,
        )

    def finish_review(self, success=True, error=False):
        """Mark our review as finished."""
        if error:
            self.github_repo.create_status(
                state="error",
                description="Static analysis error! inline-plz failed to run.",
                context="inline-plz",
                sha=self.last_sha,
            )
        elif success:
            self.github_repo.create_status(
                state="success",
                description="Static analysis complete! No errors found in your PR.",
                context="inline-plz",
                sha=self.last_sha,
            )
        else:
            self.github_repo.create_status(
                state="failure",
                description="Static analysis complete! Found errors in your PR.",
                context="inline-plz",
                sha=self.last_sha,
            )

    def out_of_date(self):
        """Check if our local latest sha matches the remote latest sha"""
        pull_request = self.github.pull_request(
            self.owner, self.repo, self.pull_request_number
        )
        latest_remote_sha = self.pr_commits(pull_request)[-1].sha
        return self.last_sha != latest_remote_sha

    def post_messages(self, messages, max_comments):
        if not self.github:
            print("Github connection is invalid.")
            return

        valid_errors = 0
        messages_posted = 0
        paths = dict()

        # randomize message order to more evenly distribute messages across different files
        messages = list(messages)
        random.shuffle(messages)
        if self.out_of_date():
            print("This run is out of date because the PR has been updated.")
            messages = []
            self.stopped_early = True
        print("Considering {} messages for posting.".format(len(messages)))
        for msg in messages:
            # rate limit
            if system.should_stop() or self.out_of_date():
                print("Stopping early.")
                self.stopped_early = True
                break

            if not msg.comments:
                continue

            msg_position = self.position(msg)
            if not msg_position:
                continue

            if msg.path.split("/")[0] in self.ignore_paths:
                continue

            paths.setdefault(msg.path, 0)

            valid_errors += 1
            self.messages_in_files.setdefault(msg.path, []).append((msg, msg_position))
            if self.is_duplicate(msg, msg_position):
                msg.status = "DUPLICATE"
                continue

            msg_at_position = self.message_at_position(msg, msg_position)
            if msg_at_position:
                try:
                    msg_at_position.edit(self.format_message(msg))
                    print("Comment edited successfully: {0}".format(msg))
                    msg.status = "EDITED"
                    paths[msg.path] += 1
                    messages_posted += 1
                    time.sleep(.1)
                    continue

                except github3.GitHubError:
                    pass

            try:
                self.pull_request.create_review_comment(
                    self.format_message(msg), self.last_sha, msg.path, msg_position
                )
                msg.status = "POSTED"
            except github3.GitHubError:
                # workaround for our diff not entirely matching up with github's diff
                # we can end up with a mismatched diff if the branch is old
                valid_errors -= 1
                continue

            print("Comment posted successfully: {0}".format(msg))
            paths[msg.path] += 1
            messages_posted += 1
            time.sleep(.1)
            if max_comments and messages_posted > max_comments:
                self.stopped_early = True
                break

        print("\n{} messages posted to Github.".format(messages_posted))
        return valid_errors

    def is_duplicate(self, message, position):
        msg = self.message_at_position(message, position)
        if msg and msg.body.strip() == self.format_message(message).strip():
            return msg
        return None

    def message_at_position(self, message, position):
        # update our list of review comments about once a second
        # to reduce dupes without hitting the API too hard
        if time.time() - self.last_update > 1:
            self.review_comments = list(self.pull_request.review_comments())
            self.last_update = time.time()
        for comment in self.review_comments:
            if comment.original_position == position and comment.path == message.path:
                return comment

        return None

    def format_message(self, message):
        if not message.comments:
            return ""

        if len(message.comments) > 1 or any("\n" in c for c in message.comments):
            return (
                "{0}: \n```\n".format(self.prefix)
                + "\n".join(sorted(list(message.comments)))
                + "\n```"
            )

        return "{0}: `{1}`".format(self.prefix, list(message.comments)[0].strip())

    def clear_outdated_messages(self):
        if self.stopped_early:
            return

        comments_to_delete = []
        in_reply_to = set()

        for comment in self.pull_request.review_comments():
            try:
                # github3 0.9.6 compat
                try:
                    in_reply_to.add(comment.to_json().get("in_reply_to_id"))
                except AttributeError:
                    in_reply_to.add(comment.as_dict().get("in_reply_to_id"))
                should_delete = True
                if not comment.body.startswith(self.prefix):
                    continue

                for msg, msg_position in self.messages_in_files.get(comment.path, []):
                    if (
                        self.format_message(msg).strip() == comment.body.strip()
                        and msg_position == comment.position
                    ):
                        should_delete = False
                if should_delete:
                    comments_to_delete.append(comment)

            except Exception:
                traceback.print_exc()

        for comment in comments_to_delete:
            try:
                if comment.id not in in_reply_to:
                    comment.delete()
                    print("Deleted comment: {}".format(comment.body))
                elif "**OBSOLETE**" not in comment.body:
                    comment.edit(comment.body + "\n**OBSOLETE**")
                    print("Edited obsolete comment: {}".format(comment.body))
            except Exception:
                traceback.print_exc()

    def position(self, message):
        """Calculate position within the PR, which is not the line number"""
        if not message.line_number:
            message.line_number = 1
        for patched_file in self.patch:
            target = patched_file.target_file.lstrip("b/")
            if target == message.path:
                offset = 1
                for hunk in patched_file:
                    for position, hunk_line in enumerate(hunk):
                        if hunk_line.target_line_no == message.line_number:
                            if not hunk_line.is_added:
                                # if the line isn't an added line, we don't want to comment on it
                                return

                            return position + offset

                    offset += len(hunk) + 1
