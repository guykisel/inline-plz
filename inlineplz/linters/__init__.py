# -*- coding: utf-8 -*-

"""Linter configurations."""

from __future__ import absolute_import

import os
import subprocess
import traceback

from inlineplz import parsers

LINTERS = {
    'prospector': {
        'install': ['pip', 'install', 'prospector'],
        'run': ['prospector', '--zero-exit'],
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
    'jslint': {
        'install': ['npm', 'install', '-g', 'jslint'],
        'run': ['jslint'],
        'dotfiles': ['.jslintrc'],
        'parser': parsers.JSLintParser
    },
    'jscs': {
        'install': ['npm', 'install', '-g', 'jscs'],
        'run': ['jscs'],
        'dotfiles': ['.jscsrc'],
        'parser': parsers.JSCSParser
    }
}


def lint():
    messages = []
    for config in LINTERS.values():
        if any(dotfile in os.listdir(os.getcwd())
               for dotfile in config.get('dotfiles')):
            try:
                output = subprocess.check_output(config.get('run')).decode('utf-8')
                messages.extend(config.get('parser')().parse(output))
            except subprocess.CalledProcessError:
                traceback.print_exc()
    return messages
