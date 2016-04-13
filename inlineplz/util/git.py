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
    ).strip()


def parent_sha(sha):
    return subprocess.check_output(
        ['git', 'rev-list', '--parents', '-n', '1', sha]
    ).strip().split()[1]
