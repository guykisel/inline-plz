# -*- coding: utf-8 -*-

import os
import subprocess
import tempfile


def current_sha():
    return (
        subprocess.check_output(["git", "rev-parse", "HEAD"], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def diff(start, end):
    return subprocess.check_output(
        ["git", "diff", "-M", "{}..{}".format(start, end)], env=os.environ
    ).decode("utf-8", errors="replace")


def parent_sha(sha):
    return (
        subprocess.check_output(["git", "rev-list", "--parents", "-n", "1", sha], env=os.environ)
        .strip()
        .split()[1]
        .decode("utf-8", errors="replace")
    )


def current_branch():
    return (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def url():
    return (
        subprocess.check_output(["git", "config", "--get", "remote.origin.url"], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def fetch(git_url):
    return (
        subprocess.check_output(["git", "fetch", git_url], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def add(filename):
    return (
        subprocess.check_output(["git", "add", filename], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def commit(message):
    return (
        subprocess.check_output(["git", "commit", "-m", message], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def push(branch):
    return (
        subprocess.check_output(["git", "push", "origin", "{}".format(branch)], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def files_changed(files):
    files_with_changes = []
    for filename in files:
        if (
            subprocess.check_output(["git", "diff", "--name-only", filename], env=os.environ)
            .strip()
            .decode("utf-8", errors="replace")
        ):
            files_with_changes.append(filename)
    return files_with_changes


def set_remote(remote):
    return (
        subprocess.check_output(["git", "config", "remote.origin.url", remote], env=os.environ)
        .strip()
        .decode("utf-8", errors="replace")
    )


def command(*args):
    git_command = ["git"]
    git_command.extend(args)
    return (
        subprocess.check_output(git_command, env=os.environ).strip().decode("utf-8", errors="replace")
    )


def clone(url, dir=None, token=None, ref=None):
    if not dir:
        dir = os.getcwd()
    if token:
        # https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth
        url = url.replace("https://", "https://{}@".format(token))
    print("Cloning: {}".format(url))
    try:
        os.makedirs(dir)
    except OSError:
        pass
    try:
        subprocess.check_call(["git", "init"], cwd=dir)

        pull_cmd = ["git", "pull", url]
        if ref:
            pull_cmd.append(ref)
        subprocess.check_call(pull_cmd, cwd=dir)
        return True
    except subprocess.CalledProcessError:
        return False


def clone_dotfiles(url, org, token=None):
    dotfile_dir = tempfile.mkdtemp()
    for repo in ["dotfiles", ".dotfiles", ".github"]:
        clone_url = "/".join([url, org, repo]) + ".git"
        print("Cloning: {}".format(clone_url))
        dotfile_path = os.path.join(dotfile_dir, repo)
        if clone(clone_url, dotfile_path, token):
            return dotfile_path
