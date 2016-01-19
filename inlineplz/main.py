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

    return inline(args)


def inline(args):
    """
    Parse input file with the specified parser and post messages based on lint output

    :param args: Contains the following
        filename: Linter output
        parser: Use a different parser based on the lint tool
        interface: How are we going to post comments?
        owner: Username of repo owner
        repo: Repository name
        pr: Pull request ID
        token: Authentication for repository
        url: Root URL of repository (not your project) Default: https://github.com
        dryrun: Prints instead of posting comments.
        zero_exit: If true: always return a 0 exit code.
    :return: Exit code. 1 if there are any comments, 0 if there are none.
    """
    if args.repo_slug:
        owner = args.repo_slug.split('/')[0]
        repo = args.repo_slug.split('/')[1]
    else:
        owner = args.owner
        repo = args.repo

    with open(args.filename) as inputfile:
        my_parser = parsers.PARSERS[args.parser]()
        messages = my_parser.parse(inputfile.read())
    # TODO: implement dryrun as an interface instead of a special case here
    if args.dryrun:
        for msg in messages:
            print(str(msg))
        return 0
    my_interface = interfaces.INTERFACES[args.interface](owner, repo, args.pr, args.token, args.url)
    if my_interface.post_messages(messages) and not args.zero_exit:
        return 1
    return 0







def this_is_a_rather_long_function_name_that_we_probably_should_not_have_here(*args):
    '''Sometimes I like to use single quotes even though that's a bad thing to do
    I also don't have a summary line separated by a blank line'''

# Lol whitespace
    def a(f):
        print f
    try:
        raise LolException('what is this even')
    except:
        a('oops')

    def FunctionNamesShouldNotLookLikeThis(this=None,more, bad, stuff):
        pass
        f = 'foo'
        b='bar'
        print 'lol this never happens'





if __name__ == "__main__":
    exit(main())
