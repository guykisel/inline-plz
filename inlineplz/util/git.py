# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess


def current_sha():
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).strip()


def diff(start, end):
    return subprocess.check_output(
        ['git', 'diff', '-M', start + '..' + end]
    )


def parent_sha(sha):
    return subprocess.check_output(
        ['git', 'rev-list', '--parents', '-n', '1', sha]
    ).strip().split()[1]


def current_branch():
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    ).strip()


def url():
    return subprocess.check_output(
        ['git', 'config', '--get', 'remote.origin.url']
    ).strip()
