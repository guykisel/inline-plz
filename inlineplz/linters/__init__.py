# -*- coding: utf-8 -*-
# pylint: disable=W0703,C0412

"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
from multiprocessing.pool import ThreadPool as Pool
import os.path
import subprocess
import sys
import time
import traceback

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk # noqa

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
    'stylus': ['*.styl'],
    'robotframework': ['*.robot'],
    'gherkin': ['*.feature']
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
            '.eslintrc.yaml',
            '.eslintignore',
            '.eslintrc',
            '.eslintrc.js',
            '.eslintrc.json'
        ],
        'parser': parsers.ESLintParser,
        'language': 'javascript',
        'autorun': True,
        'run_per_file': False
    },
    'gherkin-lint': {
        'install': [['npm', 'install'], ['npm', 'install', 'gherkin-lint']],
        'help': [os.path.normpath('./node_modules/.bin/gherkin-lint'), '--help'],
        'run': [os.path.normpath('./node_modules/.bin/gherkin-lint'), '.', '-f', 'json'],
        'rundefault': [os.path.normpath('./node_modules/.bin/gherkin-lint'), '.', '-f', 'json', '-c',
                       '{config_dir}/.gherkin-lintrc'],
        'dotfiles': [
            '.gherkin-lintrc'
        ],
        'parser': parsers.GherkinLintParser,
        'language': 'gherkin',
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
        'autorun': False,
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
        'help': ['yaml-lint'],
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
        'rundefault': ['mdl', '.', '-c', '{config_dir}/.mdlrc'],
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
        'dotfiles': ['.stylintrc'],
        'parser': parsers.StylintParser,
        'language': 'stylus',
        'autorun': True,
        'run_per_file': False
    },
    'rflint': {
        'install': [['pip', 'install', 'robotframework-lint']],
        'help': ['rflint', '--help'],
        'run': ['rflint'],
        'rundefault': ['rflint', '-A', '{config_dir}/.rflint'],
        'dotfiles': ['.rflint'],
        'parser': parsers.RobotFrameworkLintParser,
        'language': 'robotframework',
        'autorun': True,
        'run_per_file': True
    },
}


def run_command(command, log_on_fail=False, log_all=False):
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
    stdout = stdout.decode('utf-8', errors='replace')
    stderr = stderr.decode('utf-8', errors='replace')
    output = '{}\n{}'.format(stdout, stderr).strip()
    if (log_on_fail and proc.returncode) or log_all:
        print(output.encode('ascii', errors='replace'))
        sys.stdout.flush()
    return proc.returncode, output


def performance_hacks():
    # https://github.com/npm/npm/issues/11283
    # npm's progress bar makes npm installs much slower
    try:
        run_command(['npm', 'set', 'progress=false'])
    except Exception:
        pass


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
    cmd = run_config(config, config_dir)
    print(cmd)
    run_cmds = []
    patterns = PATTERNS.get(config.get('language'))
    paths = all_filenames_in_dir(path=path, ignore_paths=ignore_paths)
    for pattern in patterns:
        for filepath in fnmatch.filter(paths, pattern):
            run_cmds.append(cmd + [filepath])
    pool = Pool()

    def result(run_cmd):
        _, out = run_command(run_cmd)
        return run_cmd[-1], out

    output = pool.map(result, run_cmds)
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
        filenames = all_filenames_in_dir(path=os.getcwd(), ignore_paths=ignore_paths)
        for linter, config in LINTERS.items():
            if not dotfilefound.get(config.get('language')) and should_autorun(config, filenames):
                linters.add(linter)
    return linters


def all_filenames_in_dir(path=None, ignore_paths=None):
    path = path or os.getcwd()
    # http://stackoverflow.com/a/2186565
    paths = set()
    for root, dirnames, filenames in os.walk(path, topdown=True):
        try:
            for ignore in ignore_paths:
                dirnames.remove(ignore)
        except ValueError:
            pass
        if should_ignore_path(root, ignore_paths):
            continue
        for filename in filenames:
            paths.add(os.path.join(root, filename))
    return paths


def should_autorun(config, filenames):
    patterns = PATTERNS.get(config.get('language'))
    if config.get('autorun'):
        for pattern in patterns:
            if fnmatch.filter(filenames, pattern):
                return True
    return False


def dotfiles_exist(config, path=None):
    path = path or os.getcwd()
    return any(dotfile.strip() in os.listdir(path) for dotfile in config.get('dotfiles'))


PREVIOUS_INSTALL_COMMANDS = []


def install_linter(config):
    for install_cmd in config.get('install'):
        if install_cmd in PREVIOUS_INSTALL_COMMANDS:
            continue
        PREVIOUS_INSTALL_COMMANDS.append(install_cmd)
        if not installed(config):
            try:
                run_command(install_cmd, log_all=True)
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
    performance_hacks()
    for linter in linters_to_run(install, autorun, ignore_paths):
        print('Running linter: {0}'.format(linter))
        sys.stdout.flush()
        start = time.time()
        output = ''
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
            print(str(output).encode('ascii', errors='replace'))
        print('Installation and running of {0} took {1} seconds'.format(linter, int(time.time() - start)))
        sys.stdout.flush()
        start = time.time()
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
            print(str(output).encode('ascii', errors='replace'))
        print('Parsing of {0} took {1} seconds'.format(linter, int(time.time() - start)))
    return messages.get_messages()
