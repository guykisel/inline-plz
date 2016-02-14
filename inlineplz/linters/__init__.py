# -*- coding: utf-8 -*-
# pylint: disable=W0703

"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function

import fnmatch
import os
import subprocess
import traceback

from inlineplz import parsers
from inlineplz import message


HERE = os.path.dirname(__file__)


PATTERNS = {
    'python': ['*.py'],
    'javascript': ['*.js'],
    'json': ['*.json'],
    'yaml': ['*.yaml', '*.yml']
}


LINTERS = {
    'prospector': {
        'install': [['pip', 'install', 'prospector']],
        'help': ['prospector', '-h'],
        'run': ['prospector', '--zero-exit', '-o', 'json'],
        'rundefault': ['prospector', '--zero-exit', '-o', 'json', '-P',
                       os.path.abspath(os.path.join(HERE, 'config', '.prospector.yaml'))],
        'dotfiles': ['.prospector.yaml'],
        'parser': parsers.ProspectorParser,
        'language': 'python',
        'autorun': True,
        'run_per_file': False
    },
    'eslint': {
        'install': [['npm', 'install'], ['npm', 'install', 'eslint']],
        'help': [os.path.normpath('./node_modules/.bin/eslint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'json'],
        'rundefault': [os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'json', '-c',
                       os.path.abspath(os.path.join(HERE, 'config', '.eslintrc'))],
        'dotfiles': [
            '.eslintrc.yml',
            '.eslintignore',
            '.eslintrc',
            'eslintrc.yml'
        ],
        'parser': parsers.ESLintParser,
        'language': 'javascript',
        'autorun': True,
        'run_per_file': False
    },
    'jshint': {
        'install': [['npm', 'install'], ['npm', 'install', 'jshint']],
        'help': [os.path.normpath('./node_modules/.bin/jshint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/jshint'), '.', '--reporter', 'checkstyle'],
        'rundefault': [os.path.normpath('./node_modules/.bin/jshint'), '.', '--reporter', 'checkstyle', '-c',
                       os.path.abspath(os.path.join(HERE, 'config', '.jshintrc'))],
        'dotfiles': ['.jshintrc'],
        'parser': parsers.JSHintParser,
        'language': 'javascript',
        'autorun': False,
        'run_per_file': False
    },
    'jscs': {
        'install': [['npm', 'install'], ['npm', 'install', 'jscs']],
        'help': [os.path.normpath('./node_modules/.bin/jscs'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json', '-m', '-1', '-v'],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json', '-m', '-1', '-v', '-c',
            os.path.abspath(os.path.join(HERE, 'config', '.jscsrc'))
        ],
        'dotfiles': ['.jscsrc', '.jscs.json'],
        'parser': parsers.JSCSParser,
        'language': 'javascript',
        'autorun': True,
        'run_per_file': False
    },
    'jsonlint': {
        'install': [['npm', 'install'], ['npm', 'install', 'jsonlint']],
        'help': [os.path.normpath('./node_modules/.bin/jsonlint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/jsonlint'), '-c', '-q'],
        'rundefault': [os.path.normpath('./node_modules/.bin/jsonlint'), '-c', '-q'],
        'dotfiles': [],
        'parser': parsers.JSONLintParser,
        'language': 'json',
        'autorun': True,
        'run_per_file': True
    },
    'yaml-lint': {
        'install': [['gem', 'install', 'yaml-lint']],
        'help': ['yaml-lint', '-h'],
        'run': ['yaml-lint', '-q'],
        'rundefault': ['yaml-lint', '-q'],
        'dotfiles': [],
        'parser': parsers.YAMLLintParser,
        'language': 'yaml',
        'autorun': True,
        'run_per_file': True
    }
}


def run_per_file(config, path=None):
    path = path or os.getcwd()
    output = []
    run_cmd = config.get('run') if dotfiles_exist(config) else config.get('rundefault')
    for root, _, filenames in os.walk(path):
        patterns = PATTERNS.get(config.get('language'))
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                file_run = run_cmd + [os.path.join(root, filename)]
                try:
                    output.append((
                        os.path.join(root, filename),
                        subprocess.check_output(file_run).decode('utf-8')
                    ))
                except subprocess.CalledProcessError:
                    pass
    return output


def linters_to_run(install=False, autorun=False):
    linters = set()
    if not autorun:
        for linter, config in LINTERS.items():
            if (installed(config) or install) and dotfiles_exist(config):
                linters.add(linter)
    else:
        dotfilefound = {}
        for linter, config in LINTERS.items():
            if dotfiles_exist(config):
                dotfilefound[config.get('language')] = True
                linters.add(linter)
        for linter, config in LINTERS.items():
            if not dotfilefound.get(config.get('language')) and should_autorun(config):
                linters.add(linter)
    return linters


def recursive_glob(pattern, path=None):
    path = path or os.getcwd()
    # http://stackoverflow.com/a/2186565
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.join(root, filename))
    return matches


def should_autorun(config):
    patterns = PATTERNS.get(config.get('language'))
    return config.get('autorun') and any(recursive_glob(pattern) for pattern in patterns)


def dotfiles_exist(config):
    return any(dotfile in os.listdir(os.getcwd()) for dotfile in config.get('dotfiles'))


def install_linter(config):
    for install_cmd in config.get('install'):
        if not installed(config):
            try:
                print(install_cmd)
                subprocess.check_call(install_cmd)
            except subprocess.CalledProcessError:
                pass
        else:
            return


def installed(config):
    try:
        with open(os.devnull, 'wb') as devnull:
            subprocess.check_call(config.get('help'), stdout=devnull, stderr=devnull)
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def lint(install=False, autorun=False):
    messages = message.Messages()
    for linter in linters_to_run(install, autorun):
        print('Running linter: {0}'.format(linter))
        output = None
        config = LINTERS.get(linter)
        try:
            if (install or autorun) and config.get('install'):
                install_linter(config)
            if config.get('run_per_file'):
                output = run_per_file(config)
            else:
                run_cmd = config.get('run') if dotfiles_exist(config) else config.get('rundefault')
                print(run_cmd)
                output = subprocess.check_output(run_cmd).decode('utf-8')
        except subprocess.CalledProcessError as err:
            traceback.print_exc()
            output = err.output
        except Exception:
            traceback.print_exc()
            print(output)
        try:
            if output:
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
