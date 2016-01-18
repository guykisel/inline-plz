#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse

from inlineplz import interfaces
from inlineplz import parsers


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int)
    parser.add_argument('--owner', type=str)
    parser.add_argument('--repo', type=str)
    parser.add_argument('--repo-slug', type=str)
    parser.add_argument('--token', type=str)
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--parser', type=str, required=True, choices=parsers.PARSERS)
    parser.add_argument('--interface', type=str, choices=interfaces.INTERFACES)
    parser.add_argument('--url', type=str)
    parser.add_argument('--dryrun', action='store_true')
    parser.add_argument('--zero-exit', action='store_true')
    args = parser.parse_args()

    if args.repo_slug:
        owner = args.repo_slug.split('/')[0]
        repo = args.repo_slug.split('/')[1]
    else:
        owner = args.owner
        repo = args.repo

    return inline(
        args.filename,
        args.parser,
        args.interface,
        owner,
        repo,
        args.pr,
        args.token,
        args.url,
        args.dryrun,
        args.zero_exit
    )


def inline(filename, parser, interface, owner, repo, pr, token, url, dryrun, zero_exit):
    """
    Parse input file with the specified parser and post messages based on lint output

    :param filename:
    :param parser:
    :param interface:
    :param owner:
    :param repo:
    :param pr:
    :param token:
    :param url:
    :param dryrun:
    :param zero_exit: If true: always return a 0 exit code. Useful for CI environments
    :return: Exit code. 1 if there are any comments, 0 if there are none.
    """
    with open(filename) as inputfile:
        my_parser = parsers.PARSERS[parser]()
        messages = my_parser.parse(inputfile.read())
    # TODO: implement dryrun as an interface instead of a special case here
    if dryrun:
        for msg in messages:
            print(str(msg))
        return 0
    my_interface = interfaces.INTERFACES[interface](owner, repo, pr, token, url)
    if my_interface.post_messages(messages) and not zero_exit:
        return 1
    return 0


if __name__ == "__main__":
    exit(main())
