# -*- coding: utf-8 -*-

"""Linter configurations."""

from __future__ import absolute_import

import os
import subprocess

from inlineplz import parsers

LINTERS = {
    'prospector': {
        'run': ['prospector', '--zero-exit'],
        'dotfile': '.prospector.yaml',
        'parser': parsers.ProspectorParser
    }
}


def lint():
    messages = []
    for config in LINTERS.values():
        if config.get('dotfile') in os.listdir(os.getcwd()):
            output = subprocess.check_output(config.get('run')).decode('utf-8')
            messages.extend(config.get('parser')().parse(output))
    return messages
