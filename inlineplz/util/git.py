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


def add(filename):
    return (
        subprocess.check_output(["git", "add", filename])
        .strip()
        .decode("utf-8", errors="replace")
    )


def commit(message):
    return (
        subprocess.check_output(["git", "commit", "-m", message])
        .strip()
        .decode("utf-8", errors="replace")
    )


def push(branch):
    return (
        subprocess.check_output(["git", "push", "origin", "HEAD:{}".format(branch)])
        .strip()
        .decode("utf-8", errors="replace")
    )


def files_changed():
    return (
        subprocess.check_output(["git", "status", "--porcelain"])
        .strip()
        .decode("utf-8", errors="replace")
    )
