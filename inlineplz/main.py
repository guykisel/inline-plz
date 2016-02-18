#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

import argparse

import yaml

from inlineplz import interfaces
from inlineplz import env
from inlineplz import linters


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pull-request', type=int)
    parser.add_argument('--owner', type=str)
    parser.add_argument('--repo', type=str)
    parser.add_argument('--repo-slug', type=str)
    parser.add_argument('--token', type=str)
    parser.add_argument('--interface', type=str, choices=interfaces.INTERFACES)
    parser.add_argument('--url', type=str)
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--zero-exit', action='store_true')
    parser.add_argument('--install', action='store_true')
    parser.add_argument('--max-comments', default=25, type=int, help='maximum comments to write')
    parser.add_argument('--autorun', action='store_true',
                        help='automatically run linters with reasonable defaults')
    args = parser.parse_args()
    args = env.update_args(args)

    return inline(args)


def update_from_config(args, config):
    for key, value in config.items():
        if not key.startswith('_'):
            args.__dict__[key] = args.__dict__.get(key) or value
    return args


def load_config(args):
    """Load inline-plz config from yaml config file with reasonable defaults."""
    config = {}
    try:
        with open('.inlineplz.yml') as configfile:
            try:
                config = yaml.safe_load(configfile) or {}
            except yaml.parser.ParserError:
                pass
    except (IOError, OSError):
        pass
    args = update_from_config(args, config)
    args.ignore_paths = args.__dict__.get('ignore_paths') or ['node_modules']
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
    if args.repo_slug:
        owner = args.repo_slug.split('/')[0]
        repo = args.repo_slug.split('/')[1]
    else:
        owner = args.owner
        repo = args.repo
    args = load_config(args)
    messages = linters.lint(args.install, args.autorun, args.ignore_paths)

    # TODO: implement dryrun as an interface instead of a special case here
    if args.dryrun:
        print_messages(messages)
        for msg in messages:
            print(str(msg))
        return 0
    try:
        my_interface = interfaces.INTERFACES[args.interface](
            owner,
            repo,
            args.pull_request,
            args.token,
            args.url
        )
        if my_interface.post_messages(messages, args.max_comments) and not args.zero_exit:
            return 1
    except KeyError:
        print_messages(messages)
    if messages and not args.zero_exit:
        return 1
    return 0


def print_messages(messages):
    for msg in sorted([str(msg) for msg in messages]):
        print(msg)


if __name__ == "__main__":
    exit(main())
