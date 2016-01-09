#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import argparse

import inlineplz.interfaces as interfaces
import inlineplz.parsers as parsers

def inline(filename, owner, repo, pr, user, token):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--pr', type=int, required=True)
    parser.add_argument('--owner', type=str, required=True)
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--token')
    parser.add_argument('--user', type=str)
    parser.add_argument('--filename', type=str, required=True)
    parser.add_argument('--parser', type=str, required=True, choices=parsers.PARSERS)
    parser.add_argument('--interface', type=str, required=True, choices=interfaces.INTERFACES)

    args = parser.parse_args()
    inline(args.filename, args.owner, args.repo, args.pr, args.user, args.token)
