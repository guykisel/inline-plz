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
    'yaml': ['*.yaml', '*.yml'],
    'rst': ['*.rst'],
    'markdown': ['*.md'],
    'stylus': ['*.styl']
}


LINTERS = {
    'prospector': {
        'install': [['pip', 'install', 'prospector']],
        'help': ['prospector', '-h'],
        'run': ['prospector', '--zero-exit', '-o', 'json'],
        'rundefault': ['prospector', '--zero-exit', '-o', 'json', '-P',
                       '{config_dir}/.prospector.yaml'],
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
                       '{config_dir}/.eslintrc'],
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
                       '{config_dir}/.jshintrc'],
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
            os.path.normpath('./node_modules/.bin/jscs'),
            '.', '-r', 'json', '-m', '-1', '-v', '-c',
            '{config_dir}/.jscsrc'
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
    },
    'rst-lint': {
        'install': [['pip', 'install', 'restructuredtext_lint']],
        'help': ['rst-lint', '-h'],
        'run': ['rst-lint', '--format', 'json'],
        'rundefault': ['rst-lint', '--format', 'json'],
        'dotfiles': [],
        'parser': parsers.RSTLintParser,
        'language': 'rst',
        'autorun': True,
        'run_per_file': True
    },
    'markdownlint': {
        'install': [['gem', 'install', 'mdl']],
        'help': ['mdl', '-h'],
        'run': ['mdl', '.'],
        'rundefault': ['mdl', '.', '{config_dir}/.mdlrc'],
        'dotfiles': ['.mdlrc'],
        'parser': parsers.MarkdownLintParser,
        'language': 'markdown',
        'autorun': True,
        'run_per_file': False
    },
    'stylint': {
        'install': [['npm', 'install'], ['npm', 'install', 'stylint']],
        'help': [os.path.normpath('./node_modules/.bin/stylint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/stylint')],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/stylint'),
            '-c',
            '{config_dir}/.stylintrc'
        ],
        'dotfiles': ['.stylintrc '],
        'parser': parsers.StylintParser,
        'language': 'stylus',
        'autorun': True,
        'run_per_file': False
    },
}


def run_command(command, log_on_fail=False):
    shell = False
    if os.name == 'nt':
        shell = True
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell,
        env=os.environ
    )
    stdout, stderr = proc.communicate()
    if stdout:
        stdout = stdout.decode('utf-8')
    if stderr:
        stderr = stderr.decode('utf-8')
    if log_on_fail and proc.returncode != 0:
        print((stdout or '') + (stderr or ''))
    return proc.returncode, (stdout or '') + (stderr or '')


def should_ignore_path(path, ignore_paths):
    for ignore_path in ignore_paths:
        if (
            os.path.relpath(path).startswith(ignore_path) or
            path.startswith(ignore_path) or
            fnmatch.fnmatch(path, ignore_path)
        ):
            return True
    return False


def run_per_file(config, ignore_paths=None, path=None, config_dir=None):
    ignore_paths = ignore_paths or []
    path = path or os.getcwd()
    output = []
    cmd = run_config(config, config_dir)
    print(cmd)
    for root, _, filenames in os.walk(path):
        if should_ignore_path(root, ignore_paths):
            continue
        patterns = PATTERNS.get(config.get('language'))
        for pattern in patterns:
            for filename in fnmatch.filter(filenames, pattern):
                if should_ignore_path(filename, ignore_paths):
                    continue
                file_run = cmd + [os.path.join(root, filename)]
                _, result = run_command(file_run)
                output.append((
                    os.path.join(root, filename),
                    result
                ))
    return output


def linters_to_run(install=False, autorun=False, ignore_paths=None):
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
            if not dotfilefound.get(config.get('language')) and should_autorun(config, ignore_paths):
                linters.add(linter)
    return linters


def recursive_glob(pattern, ignore_paths=None, path=None):
    path = path or os.getcwd()
    # http://stackoverflow.com/a/2186565
    matches = []
    for root, _, filenames in os.walk(path):
        if should_ignore_path(root, ignore_paths):
            continue
        for filename in fnmatch.filter(filenames, pattern):
            if should_ignore_path(filename, ignore_paths):
                continue
            matches.append(os.path.join(root, filename))
    return matches


def should_autorun(config, ignore_paths=None):
    patterns = PATTERNS.get(config.get('language'))
    return config.get('autorun') and any(recursive_glob(pattern, ignore_paths) for pattern in patterns)


def dotfiles_exist(config, path=None):
    path = path or os.getcwd()
    return any(dotfile in os.listdir(path) for dotfile in config.get('dotfiles'))


PREVIOUS_INSTALL_COMMANDS = []


def install_linter(config):
    for install_cmd in config.get('install'):
        if install_cmd in PREVIOUS_INSTALL_COMMANDS:
            continue
        PREVIOUS_INSTALL_COMMANDS.append(install_cmd)
        if not installed(config):
            try:
                run_command(install_cmd, log_on_fail=True)
            except OSError:
                print('Install failed: {0}\n{1}'.format(install_cmd, traceback.format_exc()))
        else:
            return


def installed(config):
    try:
        returncode, _ = run_command(config.get('help'))
        return returncode == 0
    except (subprocess.CalledProcessError, OSError):
        return False


def run_config(config, config_dir):
    if dotfiles_exist(config) and config.get('run'):
        return config.get('run')
    if not (config_dir and dotfiles_exist(config, config_dir)):
        config_dir = os.path.abspath(os.path.join(HERE, 'config'))
    return [
        os.path.normpath(item.format(config_dir=config_dir))
        for item in (config.get('rundefault') or config.get('run'))
    ]


def lint(install=False, autorun=False, ignore_paths=None, config_dir=None):
    messages = message.Messages()
    for linter in linters_to_run(install, autorun, ignore_paths):
        print('Running linter: {0}'.format(linter))
        output = None
        config = LINTERS.get(linter)
        try:
            if (install or autorun) and config.get('install'):
                install_linter(config)
            if config.get('run_per_file'):
                output = run_per_file(config, ignore_paths, config_dir)
            else:
                cmd = run_config(config, config_dir)
                print(cmd)
                _, output = run_command(cmd)
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
