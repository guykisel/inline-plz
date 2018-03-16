# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import subprocess


def current_sha():
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD']
    ).strip().decode('utf-8', errors='replace')


def diff(start, end):
    return subprocess.check_output(
        ['git', 'diff', '-M', start + '..' + end]
    ).strip().decode('utf-8', errors='replace')


def parent_sha(sha):
    return subprocess.check_output(
        ['git', 'rev-list', '--parents', '-n', '1', sha]
    ).strip().decode('utf-8', errors='replace').split()[1]


def current_branch():
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD']
    ).strip().decode('utf-8', errors='replace')
