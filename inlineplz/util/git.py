# -*- coding: utf-8 -*-

import subprocess


def current_sha():
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"])
        .strip()
        .decode("utf-8", errors="replace")
    )


def diff(start, end):
    return subprocess.check_output(
        ["git", "diff", "-M", "{}..{}".format(start, end)]
    ).decode("utf-8", errors="replace")


def parent_sha(sha):
    return (
        subprocess.check_output(["git", "rev-list", "--parents", "-n", "1", sha])
        .strip()
        .split()[1]
        .decode("utf-8", errors="replace")
    )


def current_branch():
    return (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .strip()
        .decode("utf-8", errors="replace")
    )


def url():
    return (
        subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
        .strip()
        .decode("utf-8", errors="replace")
    )


def fetch(git_url):
    return (
        subprocess.check_output(["git", "fetch", git_url])
        .strip()
        .decode("utf-8", errors="replace")
    )
