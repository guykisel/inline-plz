# -*- coding: utf-8 -*-

"""Linter configurations."""

from __future__ import absolute_import

import os
import subprocess
import traceback

from inlineplz import parsers
from inlineplz import message

LINTERS = {
    'prospector': {
        'install': ['pip', 'install', 'prospector'],
        'run': ['prospector', '--zero-exit', '-o', 'json'],
        'dotfiles': ['.prospector.yaml'],
        'parser': parsers.ProspectorParser
    },
    'eslint': {
        'install': ['npm', 'install', '-g', 'eslint'],
        'run': ['eslint', '.', '-f', 'json'],
        'dotfiles': [
            '.eslintrc.yml',
            '.eslintignore',
            '.eslintrc',
            'eslintrc.yml'
        ],
        'parser': parsers.ESLintParser
    },
    'jshint': {
        'install': ['npm', 'install', '-g', 'jshint'],
        'run': ['jshint'],
        'dotfiles': ['.jshintrc'],
        'parser': parsers.JSHintParser
    },
    'jscs': {
        'install': ['npm', 'install', '-g', 'jscs'],
        'run': ['jscs', '.', '-r', 'json', '-m', '-1', '-v'],
        'dotfiles': ['.jscsrc', '.jscs.json'],
        'parser': parsers.JSCSParser
    }
}


def lint(install=False):
    messages = message.Messages()
    for config in LINTERS.values():
        if any(dotfile in os.listdir(os.getcwd())
               for dotfile in config.get('dotfiles')):
            try:
                if install and config.get('install'):
                    subprocess.check_call(config.get('install'))
                output = subprocess.check_output(config.get('run')).decode('utf-8')
                messages.add_messages(config.get('parser')().parse(output))
            except subprocess.CalledProcessError:
                traceback.print_exc()
    return messages.get_messages()
