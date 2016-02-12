# -*- coding: utf-8 -*-
# pylint: disable=W0703

"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function

import glob
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
        'parser': parsers.ProspectorParser,
        'glob': ['*.py', '**/*.py'],
        'autorun': True
    },
    'eslint': {
        'install': ['npm', 'install'],
        'run': [os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'json'],
        'dotfiles': [
            '.eslintrc.yml',
            '.eslintignore',
            '.eslintrc',
            'eslintrc.yml'
        ],
        'parser': parsers.ESLintParser,
        'glob': ['*.js', '**/*.js'],
        'autorun': True
    },
    'jshint': {
        'install': ['npm', 'install'],
        'run': [os.path.normpath('./node_modules/.bin/jshint'), '.', '--reporter', 'checkstyle'],
        'dotfiles': ['.jshintrc'],
        'parser': parsers.JSHintParser,
        'glob': ['*.js', '**/*.js'],
        'autorun': False
    },
    'jscs': {
        'install': ['npm', 'install'],
        'run': [os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json', '-m', '-1', '-v'],
        'dotfiles': ['.jscsrc', '.jscs.json'],
        'parser': parsers.JSCSParser,
        'glob': ['*.js', '**/*.js'],
        'autorun': True
    }
}


def should_autorun(config):
    return config.get('autorun') and any(glob.glob(pattern) for pattern in config.get('glob'))


def dotfiles_exist(config):
    return any(dotfile in os.listdir(os.getcwd()) for dotfile in config.get('dotfiles'))


def lint(install=False, autorun=False):
    messages = message.Messages()
    for linter, config in LINTERS.items():
        if dotfiles_exist(config) or (autorun and should_autorun(config)):
            try:
                if (install or autorun) and config.get('install'):
                    subprocess.check_call(config.get('install'))
                print(config.get('run'))
                output = subprocess.check_output(config.get('run')).decode('utf-8')
            except subprocess.CalledProcessError as err:
                traceback.print_exc()
                output = err.output
            except Exception:
                traceback.print_exc()
                print(output)
            try:
                if output.strip():
                    linter_messages = config.get('parser')().parse(output)
                    # prepend linter name to message content
                    linter_messages = {
                        (msg[0], msg[1], '{0}: {1}'.format(linter, msg[2])) for msg in linter_messages
                    }
                    messages.add_messages(linter_messages)
            except Exception:
                traceback.print_exc()
                print(output)
    return messages.get_messages()
