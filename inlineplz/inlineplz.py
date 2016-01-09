#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse
import pprint

import inlineplz.interfaces as interfaces
import inlineplz.parsers as parsers


def inline(filename, parser, interface, owner, repo, pr, token, url, dryrun):
    with open(filename) as inputfile:
        my_parser = parsers.PARSERS[parser]()
        messages = my_parser.parse(inputfile.read())
    # TODO: implement dryrun as an interface instead of a special case here
    if dryrun:
        for msg in messages:
            pprint.pprint(msg)
        return
    my_interface = interfaces.INTERFACES[interface](owner, repo, pr, token, url)
    my_interface.post_messages(messages)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--owner', type=str, required=True)
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--token', type=str, require=True)
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--parser', type=str, required=True, choices=parsers.PARSERS)
    parser.add_argument('--interface', type=str, required=True, choices=interfaces.INTERFACES)
    parser.add_argument('--url', type=str)
    parser.add_argument('--dryrun', action='store_true')

    args = parser.parse_args()
    inline(
        args.filename,
        args.parser,
        args.interface,
        args.owner,
        args.repo,
        args.pr,
        args.token,
        args.url,
        args.dryrun
    )
