#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys
import time

import giturlparse
import yaml

from inlineplz import interfaces
from inlineplz import env
from inlineplz import linters
from inlineplz import __version__


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pull-request', type=int)
    parser.add_argument('--owner', type=str)
    parser.add_argument('--repo', type=str)
    parser.add_argument('--repo-slug', type=str)
    parser.add_argument('--branch', type=str)
    parser.add_argument('--token', type=str)
    parser.add_argument('--commit', type=str, help='commit hash or number')
    parser.add_argument('--interface', type=str, choices=interfaces.INTERFACES)
    parser.add_argument('--url', type=str)
    parser.add_argument('--enabled-linters', type=str, nargs='+')
    parser.add_argument('--disabled-linters', type=str, nargs='+')
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--zero-exit', action='store_true')
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--trusted', action='store_true', help='allow installing all local dependencies')
    parser.add_argument('--max-comments', default=25, type=int, help='maximum comments to write')
    parser.add_argument(
        '--autorun',
        action='store_true',
        help='automatically run linters with reasonable defaults'
    )
    parser.add_argument(
        '--config-dir',
        help='default directory to search for linter config files'
    )
    args = parser.parse_args()
    args = env.update_args(args)
    if args.config_dir:
        args.config_dir = os.path.abspath(args.config_dir)
        if not os.path.exists(args.config_dir):
            args.config_dir = None
    print('inline-plz version: {}'.format(__version__))
    print('Python version: {}'.format(sys.version))
    start = time.time()
    result = inline(args)
    print('inline-plz version: {}'.format(__version__))
    print('Python version: {}'.format(sys.version))
    print('inline-plz ran for {} seconds'.format(int(time.time() - start)))
    print('inline-plz returned exit code {}'.format(result))
    return result


def update_from_config(args, config):
    blacklist = [
        'trusted', 'token', 'interface', 'owner', 'repo', 'config_dir'
        'repo_slug', 'pull_request', 'zero_exit', 'dryrun', 'url', 'branch'
    ]
    for key, value in config.items():
        if not key.startswith('_') and key not in blacklist:
            args.__dict__[key] = args.__dict__.get(key) or value
    return args


def load_config(args, config_path='.inlineplz.yml'):
    """Load inline-plz config from yaml config file with reasonable defaults."""
    config = {}
    print(config_path)
    try:
        with open(config_path) as configfile:
            try:
                config = yaml.safe_load(configfile) or {}
                if config:
                    print('Loaded config from {}'.format(config_path))
            except yaml.parser.ParserError:
                pass
    except (IOError, OSError):
        pass
    args = update_from_config(args, config)
    args.ignore_paths = args.__dict__.get('ignore_paths') or [
        'node_modules', '.git', '.tox', 'godeps', 'vendor']
    if config_path != '.inlineplz.yml':
        return args
    # fall back to config_dir inlineplz yaml if we didn't find one locally
    if args.config_dir and not config:
        new_config_path = os.path.join(args.config_dir, config_path)
        if os.path.exists(new_config_path):
            return load_config(args, new_config_path)
    return args


def inline(args):
    """
    Parse input file with the specified parser and post messages based on lint output

    :param args: Contains the following
        interface: How are we going to post comments?
        owner: Username of repo owner
        repo: Repository name
        pr: Pull request ID
        token: Authentication for repository
        url: Root URL of repository (not your project) Default: https://github.com
        dryrun: Prints instead of posting comments.
        zero_exit: If true: always return a 0 exit code.
        install: If true: install linters.
        max_comments: Maximum comments to write
    :return: Exit code. 1 if there are any comments, 0 if there are none.
    """
    # don't load trusted value from config because we don't trust the config
    trusted = args.trusted
    args = load_config(args)

    # TODO: consider moving this git parsing stuff into the github interface
    url = args.url
    if args.repo_slug:
        owner = args.repo_slug.split('/')[0]
        repo = args.repo_slug.split('/')[1]
    else:
        owner = args.owner
        repo = args.repo
    if args.url:
        try:
            url_to_parse = args.url
            # giturlparse won't parse URLs that don't end in .git
            if not url_to_parse.endswith('.git'):
                url_to_parse += '.git'
            parsed = giturlparse.parse(str(url_to_parse))
            url = parsed.resource
            if not url.startswith('https://'):
                url = 'https://' + url
            if parsed.owner:
                owner = parsed.owner
            if parsed.name:
                repo = parsed.name
        except giturlparse.parser.ParserError:
            pass
    if not args.dryrun and args.interface not in interfaces.INTERFACES:
        print('Valid inline-plz config not found')
        return 1
    messages = linters.lint(
        args.install,
        args.autorun,
        args.ignore_paths,
        args.config_dir,
        args.enabled_linters,
        args.disabled_linters,
        trusted
    )
    print('{} lint messages found'.format(len(messages)))
    print('inline-plz version: {}'.format(__version__))
    print('Python version: {}'.format(sys.version))

    # TODO: implement dryrun as an interface instead of a special case here
    if args.dryrun:
        print_messages(messages)
        return 0
    try:
        print('Using interface: {0}'.format(args.interface))
        my_interface = interfaces.INTERFACES[args.interface](
            owner,
            repo,
            args.pull_request,
            args.branch,
            args.token,
            url,
            args.commit,
            args.ignore_paths
        )
        if my_interface.post_messages(messages, args.max_comments) and not args.zero_exit:
            return 1
    except KeyError:
        print('Interface not found: {}'.format(args.interface))
    return 0


def print_messages(messages):
    for msg in sorted([str(msg) for msg in messages]):
        print(msg)
    print('{} lint messages found'.format(len(messages)))


if __name__ == "__main__":
    exit(main())
