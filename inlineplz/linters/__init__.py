# -*- coding: utf-8 -*-
# pylint: disable=W0703,C0412
"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import fnmatch
from multiprocessing.pool import ThreadPool as Pool
import os.path
import shutil
import subprocess
import sys
import time
import traceback

# Use the built-in version of scandir/walk if possible, otherwise
# use the scandir module version
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk  # noqa

from inlineplz import parsers
from inlineplz import message
from inlineplz.util import system

HERE = os.path.dirname(__file__)


if sys.platform == 'win32':
    JAVA_SEP = ';'
else:
    JAVA_SEP = ':'


def vendored_path(path):
    return os.path.relpath(os.path.join(HERE, '..', 'bin', path))


# glob patterns for what language is represented by what type of files.
PATTERNS = {
    'ansible': ['*.yaml', '*.yml'],
    'docker': ['*Dockerfile', '*.dockerfile'],
    'gherkin': ['*.feature'],
    'go': ['*.go'],
    'groovy': ['*.groovy', 'Jenkinsfile', 'jenkinsfile'],
    'java': ['*.java'],
    'javascript': ['*.js'],
    'json': ['*.json'],
    'markdown': ['*.md'],
    'python': ['*.py'],
    'shell': ['*.sh', '*.zsh', '*.ksh', '*.bsh', '*.csh', '*.bash'],
    'stylus': ['*.styl'],
    'robotframework': ['*.robot'],
    'rst': ['*.rst'],
    'yaml': ['*.yaml', '*.yml']
}

# these commands will be autorun to try to install dependencies.
TRUSTED_INSTALL = [
    ['bundle', 'install'],
    ['cabal', 'update'],
    ['cabal', 'install'],
    ['glide', 'install', '--strip-vendor'],
    ['godep', 'get'],
    ['godep', 'restore'],
    ['dep', 'ensure'],
    ['dep', 'prune'],
    ['govendor', 'sync'],
    ['go', 'get', '-t', '-v', './...'],
    ['yarn', 'install', '--non-interactive'],
    ['npm', 'install'],
    ['pip', 'install', '-r', 'requirements.txt'],
    ['pip', 'install', '-r', 'requirements_dev.txt'],
    ['pipenv', 'install'],
    ['python', 'setup.py', 'develop']
]

# these dirs will get deleted after a run
INSTALL_DIRS = ['node_modules', '.bundle']

GROOVY_PATH = vendored_path(os.path.join('groovy', 'groovy-all-2.4.15.jar'))
SLF4J_PATH = vendored_path(os.path.join('groovy', 'slf4j-api-1.7.25.jar'))

# linter configs. add new tools here.
LINTERS = {
    'ansible-lint': {
        'install': [['pip', 'install', '-U', 'ansible-lint']],
        'help': ['ansible-lint', '-h'],
        'run': ['ansible-lint', '*/*.yaml', '*/*.yml', '-p'],
        'rundefault': ['ansible-lint', '*/*.yaml', '*/*.yml', '-p', '-c', '{config_dir}/.ansible-lint'],
        'dotfiles': ['.ansible-lint'],
        'parser': parsers.AnsibleLintParser,
        'language': 'ansible',
        'autorun': True,
        'run_per_file': False
    },
    'bandit': {
        'install': [['pip', 'install', '-U', 'bandit']],
        'help': ['bandit', '-h'],
        'run': ['bandit', '-f', 'json', '-iii', '-ll', '-r', '.'],
        'rundefault': [
            'bandit', '-f', 'json', '-iii', '-ll', '-r', '.', '-c',
            '{config_dir}/bandit.yaml'
        ],
        'dotfiles': ['bandit.yaml'],
        'parser': parsers.BanditParser,
        'language': 'python',
        'autorun': True,
        'run_per_file': False
    },
    'codenarc': {
        'install': [],
        'help': [
            'java',
            '-classpath',
            '{}{}{}{}{}{}{}{}{}'.format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join('codenarc', 'CodeNarc-1.1.jar')),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path('codenarc'),
                JAVA_SEP,
                '.'
            ),
            'org.codenarc.CodeNarc',
            '-help'
        ],
        'run': [
            'java',
            '-classpath',
            '{}{}{}{}{}{}{}{}{}'.format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join('codenarc', 'CodeNarc-1.1.jar')),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path('codenarc'),
                JAVA_SEP,
                '.'
            ),
            'org.codenarc.CodeNarc',
            '-includes=**/*.groovy,**/Jenkinsfile,**/jenkinsfile,**/...groovy',
            '-report=console',
            '-rulesetfiles={}'.format(os.path.join(os.getcwd(), 'codenarc.xml'))
        ],
        'rundefault': [
            'java',
            '-classpath',
            '{}{}{}{}{}{}{}{}{}'.format(
                GROOVY_PATH,
                JAVA_SEP,
                vendored_path(os.path.join('codenarc', 'CodeNarc-1.1.jar')),
                JAVA_SEP,
                SLF4J_PATH,
                JAVA_SEP,
                vendored_path('codenarc'),
                JAVA_SEP,
                '.'
            ),
            'org.codenarc.CodeNarc',
            '-includes=**/*.groovy,**/Jenkinsfile,**/jenkinsfile,**/...groovy',
            '-report=console',
            '-rulesetfiles=codenarc.xml'
        ],
        'dotfiles': ['codenarc.xml'],
        'parser': parsers.CodenarcParser,
        'language': 'groovy',
        'autorun': True,
        'run_per_file': False
    },
    'dockerfile_lint': {
        'install': [['npm', 'install', 'dockerfile_lint']],
        'help':
        [os.path.normpath('./node_modules/.bin/dockerfile_lint'), '-h'],
        'run':
        [os.path.normpath('./node_modules/.bin/dockerfile_lint'), '-j', '-f'],
        'rundefault':
        [os.path.normpath('./node_modules/.bin/dockerfile_lint'), '-j', '-f'],
        'dotfiles': [],
        'parser': parsers.DockerfileLintParser,
        'language': 'docker',
        'autorun': True,
        'run_per_file': True
    },
    'eslint': {
        'install': [['npm', 'install', 'eslint']],
        'help': [os.path.normpath('./node_modules/.bin/eslint'), '-h'],
        'run':
        [os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'unix'],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/eslint'), '.', '-f', 'unix',
            '-c', '{config_dir}/.eslintrc.js', '--ignore-path', '{config_dir}/.eslintignore'
        ],
        'dotfiles': [
            '.eslintrc.yml', '.eslintrc.yaml', '.eslintignore', '.eslintrc',
            '.eslintrc.js', '.eslintrc.json'
        ],
        'parser': parsers.ESLintParser,
        'language': 'javascript',
        'autorun': True,
        'run_per_file': False
    },
    'gherkin-lint': {
        'install': [['npm', 'install', 'gherkin-lint']],
        'help':
        [os.path.normpath('./node_modules/.bin/gherkin-lint'), '--help'],
        'run': [
            os.path.normpath('./node_modules/.bin/gherkin-lint'), '.', '-f',
            'json'
        ],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/gherkin-lint'), '.', '-f',
            'json', '-c', '{config_dir}/.gherkin-lintrc'
        ],
        'dotfiles': ['.gherkin-lintrc'],
        'parser': parsers.GherkinLintParser,
        'language': 'gherkin',
        'autorun': True,
        'run_per_file': False
    },
    'gometalinter.v2': {
        'install': [['go', 'get', '-u', 'gopkg.in/alecthomas/gometalinter.v2'],
                    ['gometalinter.v2', '--install', '--update']],
        'help': ['gometalinter.v2', '--install', '--update'],
        'run': ['gometalinter.v2', '--enable-gc', '--deadline=300s', '--aggregate', '--vendor',
                '--json', '-s', 'node_modules', '-s', 'src', './...'],
        'rundefault':
            ['gometalinter.v2', '--enable-gc', '--deadline=300s', '--aggregate', '--vendor', '--disable=lll',
             '--json', '-s', 'node_modules', '-s', 'src', '--config={config_dir}/.gometalinter.json', './...'],
        'dotfiles': ['.gometalinter.json'],
        'parser': parsers.GometalinterParser,
        'language': 'go',
        'autorun': False,
        'run_per_file': False
    },
    'gometalinter': {
        'install': [['go', 'get', '-u', 'github.com/alecthomas/gometalinter'],
                    ['gometalinter', '--install', '--update']],
        'help': ['gometalinter', '--install', '--update'],
        'run': ['gometalinter', '--enable-gc', '--deadline=300s', '--aggregate', '--vendor',
                '--json', '-s', 'node_modules', '-s', 'src', './...'],
        'rundefault':
            ['gometalinter', '--enable-gc', '--deadline=300s', '--aggregate', '--vendor', '--disable=lll',
             '--json', '-s', 'node_modules', '-s', 'src', '--config={config_dir}/.gometalinter.json', './...'],
        'dotfiles': ['.gometalinter.json'],
        'parser': parsers.GometalinterParser,
        'language': 'go',
        'autorun': True,
        'run_per_file': False
    },
    'jscs': {
        'install': [['npm', 'install', 'jscs']],
        'help': [os.path.normpath('./node_modules/.bin/jscs'), '-h'],
        'run': [
            os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json',
            '-m', '-1', '-v'
        ],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/jscs'), '.', '-r', 'json',
            '-m', '-1', '-v', '-c', '{config_dir}/.jscsrc'
        ],
        'dotfiles': ['.jscsrc', '.jscs.json'],
        'parser': parsers.JSCSParser,
        'language': 'javascript',
        'autorun': False,
        'run_per_file': False
    },
    'jshint': {
        'install': [['npm', 'install', 'jshint']],
        'help': [os.path.normpath('./node_modules/.bin/jshint'), '-h'],
        'run': [
            os.path.normpath('./node_modules/.bin/jshint'), '.', '--reporter',
            'checkstyle'
        ],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/jshint'), '.', '--reporter',
            'checkstyle', '-c', '{config_dir}/.jshintrc'
        ],
        'dotfiles': ['.jshintrc'],
        'parser': parsers.JSHintParser,
        'language': 'javascript',
        'autorun': False,
        'run_per_file': False
    },
    'jsonlint': {
        'install': [['npm', 'install', 'jsonlint']],
        'help': [os.path.normpath('./node_modules/.bin/jsonlint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/jsonlint'), '-c', '-q'],
        'rundefault':
        [os.path.normpath('./node_modules/.bin/jsonlint'), '-c', '-q'],
        'dotfiles': [],
        'parser': parsers.JSONLintParser,
        'language': 'json',
        'autorun': True,
        'run_per_file': True
    },
    'markdownlint-cli': {
        'install': [['npm', 'install', 'markdownlint-cli']],
        'help': [os.path.normpath('./node_modules/.bin/markdownlint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/markdownlint'), '.'],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/markdownlint'), '.', '-c',
            '{config_dir}/.markdownlintrc'
        ],
        'dotfiles': ['.markdownlintrc', '.markdownlint.json'],
        'parser': parsers.MarkdownLintParser,
        'language': 'markdown',
        'autorun': True,
        'run_per_file': False
    },
    'megacheck': {
        'install': [['go', 'get', '-u', 'honnef.co/go/tools/cmd/megacheck']],
        'help': ['megacheck', '--help'],
        'run': ['megacheck', '-f', 'json', './...'],
        'rundefault': ['megacheck', '-f', 'json', './...'],
        'dotfiles': [],
        'parser': parsers.MegacheckParser,
        'language': 'go',
        'autorun': False,
        'run_per_file': False
    },
    'pmd': {
        'install': [],
        'help': [vendored_path(os.path.join('pmd', 'pmd-bin-6.3.0', 'bin', 'run.sh')), '-help'],
        'run': [
            vendored_path(os.path.join('pmd', 'pmd-bin-6.3.0', 'bin', 'run.sh')),
            'pmd', '-d', '.', '-R', 'java-basic', '-f', 'emacs'
        ],
        'rundefault': [
            vendored_path(os.path.join('pmd', 'pmd-bin-6.3.0', 'bin', 'run.sh')),
            'pmd', '-d', '.', '-R', 'java-basic', '-f', 'emacs'
        ],
        'dotfiles': [],
        'parser': parsers.PMDParser,
        'language': 'java',
        'autorun': True,
        'run_per_file': False
    },
    'prospector': {
        'install': [['pip', 'install', '-U', 'prospector[with_everything]'],
                    ['pip', 'install', '-U', 'prospector']],
        'help': ['prospector', '-h'],
        'run': ['prospector', '--zero-exit', '-o', 'json'],
        'rundefault': [
            'prospector', '--zero-exit', '-o', 'json', '-P',
            '{config_dir}/.prospector.yaml'
        ],
        'dotfiles': ['.prospector.yaml'],
        'parser': parsers.ProspectorParser,
        'language': 'python',
        'autorun': True,
        'run_per_file': False
    },
    'robotframework-lint': {
        'install': [['pip', 'install', '-U', 'robotframework-lint']],
        'help': ['rflint', '--help'],
        'run': ['rflint'],
        'rundefault': ['rflint', '-A', '{config_dir}/.rflint'],
        'dotfiles': ['.rflint'],
        'parser': parsers.RobotFrameworkLintParser,
        'language': 'robotframework',
        'autorun': True,
        'run_per_file': True
    },
    'restructuredtext_lint': {
        'install': [['pip', 'install', '-U', 'restructuredtext_lint']],
        'help': ['rst-lint', '-h'],
        'run': ['rst-lint', '--format', 'json', '--encoding', 'utf-8'],
        'rundefault': ['rst-lint', '--format', 'json', '--encoding', 'utf-8'],
        'dotfiles': [],
        'parser': parsers.RSTLintParser,
        'language': 'rst',
        'autorun': True,
        'run_per_file': True
    },
    'shellcheck': {
        'install': [
            ['cabal', 'update'],
            ['cabal', 'install', 'shellcheck'],
            ['apt-get', 'install', 'shellcheck'],
            ['dnf', 'install', 'shellcheck'],
            ['brew', 'install', 'shellcheck'],
            ['port', 'install', 'shellcheck'],
            ['zypper', 'in', 'ShellCheck'],
        ],
        'help': ['shellcheck', '-V'],
        'run': ['shellcheck', '-f', 'json'],
        'rundefault': ['shellcheck', '-f', 'json'],
        'dotfiles': [],
        'parser': parsers.ShellcheckParser,
        'language': 'shell',
        'autorun': True,
        'run_per_file': True
    },
    'spotbugs-maven-plugin': {
        'install': [
            ['mvn', 'clean', 'install', '-U'],
            ['mvn', 'dependency:get', '-Dartifact=com.github.spotbugs:spotbugs-maven-plugin:3.1.3']
        ],
        'help': ['mvn', 'com.github.spotbugs:spotbugs-maven-plugin:3.1.3:help'],
        'run': ['mvn', '-Dspotbugs.failOnError=false', 'com.github.spotbugs:spotbugs-maven-plugin:3.1.3:check'],
        'rundefault': ['mvn', '-Dspotbugs.failOnError=false', 'com.github.spotbugs:spotbugs-maven-plugin:3.1.3:check'],
        'dotfiles': [],
        'parser': parsers.SpotbugsMavenParser,
        'language': 'java',
        'autorun': True,
        'run_per_file': False
    },
    'stylint': {
        'install': [['npm', 'install', 'stylint']],
        'help': [os.path.normpath('./node_modules/.bin/stylint'), '-h'],
        'run': [os.path.normpath('./node_modules/.bin/stylint')],
        'rundefault': [
            os.path.normpath('./node_modules/.bin/stylint'), '-c',
            '{config_dir}/.stylintrc'
        ],
        'dotfiles': ['.stylintrc'],
        'parser': parsers.StylintParser,
        'language': 'stylus',
        'autorun': True,
        'run_per_file': False
    },
    'yamllint': {
        'install': [['pip', 'install', 'yamllint']],
        'help': ['yamllint', '-h'],
        'run': ['yamllint', '-f', 'parsable', '.'],
        'rundefault': ['yamllint', '-c', '{config_dir}/.yamllint', '-f', 'parsable', '.'],
        'dotfiles': ['.yamllint'],
        'parser': parsers.YAMLLintParser,
        'language': 'yaml',
        'autorun': True,
        'run_per_file': False
    },
}


def run_command(command, log_on_fail=False, log_all=False):
    print('Running: "{}"'.format(' '.join(command)))
    shell = False
    if os.name == 'nt':
        shell = True
    popen_kwargs = {
        'args': command,
        'stdin': subprocess.PIPE,
        'stdout': subprocess.PIPE,
        'stderr': subprocess.PIPE,
        'shell': shell,
        'env': os.environ,
        'universal_newlines': True
    }
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 6:
        popen_kwargs['encoding'] = 'utf-8'
    proc = subprocess.Popen(**popen_kwargs)
    stdout, stderr = proc.communicate()
    output = '{}\n{}'.format(stdout, stderr).strip()
    if output and ((log_on_fail and proc.returncode) or log_all):
        print(output)
        sys.stdout.flush()
    return proc.returncode, output


def performance_hacks():
    # https://github.com/npm/npm/issues/11283
    # npm's progress bar makes npm installs much slower
    try:
        run_command(['npm', 'set', 'progress=false'])
    except Exception:
        pass


def cleanup():
    """Delete standard installation directories."""
    for install_dir in INSTALL_DIRS:
        try:
            shutil.rmtree(install_dir, ignore_errors=True)
        except Exception:
            print(traceback.format_exc())
            print('Failed to delete {}'.format(install_dir))


def should_ignore_path(path, ignore_paths):
    for ignore_path in ignore_paths:
        if (os.path.relpath(path).startswith(ignore_path) or
                path.startswith(ignore_path) or
                fnmatch.fnmatch(path, ignore_path)):
            return True
    return False


def run_per_file(config, ignore_paths=None, path=None, config_dir=None):
    ignore_paths = ignore_paths or []
    path = path or os.getcwd()
    cmd = run_config(config, config_dir)
    run_cmds = []
    patterns = PATTERNS.get(config.get('language'))
    paths = all_filenames_in_dir(path=path, ignore_paths=ignore_paths)
    for pattern in patterns:
        for filepath in fnmatch.filter(paths, pattern):
            run_cmds.append(cmd + [filepath])
    pool = Pool()

    def result(run_cmd):
        _, out = run_command(run_cmd)
        return run_cmd[-1], out.strip()

    output = pool.map(result, run_cmds)
    return output


def linters_to_run(autorun=False,
                   ignore_paths=None,
                   enabled_linters=None,
                   disabled_linters=None):
    linters = set()
    enabled_linters = enabled_linters or []
    disabled_linters = disabled_linters or []
    try:
        enabled_linters.extend(enabled_linters[0].split(','))
    except (IndexError, AttributeError):
        pass
    try:
        disabled_linters.extend(disabled_linters[0].split(','))
    except (IndexError, AttributeError):
        pass
    if not autorun:
        for linter, config in LINTERS.items():
            if linter in enabled_linters:
                linters.add(linter)
    else:
        dotfilefound = {}
        for linter, config in LINTERS.items():
            if dotfiles_exist(config) and config.get('autorun'):
                dotfilefound[config.get('language')] = True
                if linter not in disabled_linters:
                    linters.add(linter)
        filenames = all_filenames_in_dir(
            path=os.getcwd(), ignore_paths=ignore_paths)
        for linter, config in LINTERS.items():
            if linter in enabled_linters or (
                    not dotfilefound.get(config.get('language')) and
                    should_autorun(config, filenames)):
                if linter not in disabled_linters:
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
    return any(dotfile.strip() in os.listdir(path)
               for dotfile in config.get('dotfiles'))


# track commands we've already run so that we don't re-run them
PREVIOUS_INSTALL_COMMANDS = []


def install_linter(config):
    install_cmds = config.get('install')
    for install_cmd in install_cmds:
        if install_cmd in PREVIOUS_INSTALL_COMMANDS:
            continue
        PREVIOUS_INSTALL_COMMANDS.append(install_cmd)
        if not installed(config):
            try:
                print('-' * 80)
                run_command(install_cmd, log_all=True)
            except OSError:
                print('Install failed: {0}\n{1}'.format(
                    install_cmd, traceback.format_exc()))
        else:
            return


def install_trusted():
    for install_cmd in TRUSTED_INSTALL:
        try:
            print('*' * 80)
            run_command(install_cmd, log_all=True)
        except OSError:
            print('Install failed: {0}\n{1}'.format(install_cmd,
                                                    traceback.format_exc()))


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
        if '...' not in item else item.format(config_dir=config_dir)
        for item in (config.get('rundefault') or config.get('run'))
    ]


def lint(install=False,
         autorun=False,
         ignore_paths=None,
         config_dir=None,
         enabled_linters=None,
         disabled_linters=None,
         trusted=False):
    messages = message.Messages()
    cleanup()
    performance_hacks()
    if trusted and (install or autorun):
        install_trusted()
    for linter in linters_to_run(autorun, ignore_paths,
                                 enabled_linters, disabled_linters):
        if system.should_stop():
            return messages.get_messages()
        print('=' * 80)
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
                _, output = run_command(cmd)
                output = output.strip()
        except Exception:
            print('Running {0} failed:'.format(linter))
            print(traceback.format_exc())
            print('Failed {0} output: {1}'.format(linter, output))
        print('Installation and running of {0} took {1} seconds'.format(
            linter, int(time.time() - start)))
        sys.stdout.flush()
        start = time.time()
        try:
            if output:
                linter_messages = config.get('parser')().parse(output)
                print('Found {0} messages from {1}'.format(len(linter_messages), linter))
                # prepend linter name to message content
                linter_messages = {
                    (msg[0], msg[1], '{0}: {1}'.format(linter, msg[2]))
                    for msg in linter_messages
                }
                messages.add_messages(linter_messages)
        except Exception:
            print('Parsing {0} output failed:'.format(linter))
            print(traceback.format_exc())
            print(output)
        print('Parsing of {0} took {1} seconds'.format(
            linter, int(time.time() - start)))
    return messages.get_messages()
