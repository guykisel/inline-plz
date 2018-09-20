# -*- coding: utf-8 -*-

"""Set up args based on envvars."""

import os

from ..env import jenkins, local, travis


def current_env():
    if os.environ.get("TRAVIS"):
        return travis.Travis()

    elif os.environ.get("JENKINS_URL"):
        return jenkins.Jenkins()

    return local.Local()


def update_args(args):
    env = current_env()
    for key, value in env.__dict__.items():
        if not key.startswith("_"):
            args.__dict__[key] = args.__dict__.get(key) or value
    return args
