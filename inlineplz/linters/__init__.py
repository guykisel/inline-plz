# -*- coding: utf-8 -*-

"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function

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
        'install': ['npm', 'install', 'eslint'],
        'run': [os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'json'],
        'dotfiles': [
            '.eslintrc.yml',
            '.eslintignore',
            '.eslintrc',
            'eslintrc.yml'
        ],
        'parser': parsers.ESLintParser
    },
    'jshint': {
        'install': ['npm', 'install', 'jshint'],
        'run': [os.path.normpath('./node_modules/.bin/jshint')],
        'dotfiles': ['.jshintrc'],
        'parser': parsers.JSHintParser
    },
    'jscs': {
        'install': ['npm', 'install', 'jscs'],
        'run': [os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json', '-m', '-1', '-v'],
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
            except subprocess.CalledProcessError as err:
                traceback.print_exc()
                output = err.output
            try:
                if output.strip():
                    messages.add_messages(config.get('parser')().parse(output))
            except ValueError:
                traceback.print_exc()
                print(output)
    return messages.get_messages()
