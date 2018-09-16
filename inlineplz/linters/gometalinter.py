# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="gometalinter",
    install=[
        ["go", "get", "-u", "github.com/alecthomas/gometalinter"],
        ["gometalinter", "--install", "--update"],
    ],
    help_cmd=["gometalinter", "--install", "--update"],
    run=[
        "gometalinter",
        "--enable-gc",
        "--deadline=300s",
        "--aggregate",
        "--vendor",
        "--json",
        "-s",
        "node_modules",
        "-s",
        "src",
        "./...",
    ],
    rundefault=[
        "gometalinter",
        "--enable-gc",
        "--deadline=300s",
        "--aggregate",
        "--vendor",
        "--disable=lll",
        "--json",
        "-s",
        "node_modules",
        "-s",
        "src",
        "--config={config_dir}/.gometalinter.json",
        "./...",
    ],
    dotfiles=[".gometalinter.json"],
    language="go",
    autorun=True,
    run_per_file=False,
)
@linter(
    name="gometalinter.v2",
    install=[
        ["go", "get", "-u", "gopkg.in/alecthomas/gometalinter.v2"],
        ["gometalinter.v2", "--install", "--update"],
    ],
    help_cmd=["gometalinter.v2", "--install", "--update"],
    run=[
        "gometalinter.v2",
        "--enable-gc",
        "--deadline=300s",
        "--aggregate",
        "--vendor",
        "--json",
        "-s",
        "node_modules",
        "-s",
        "src",
        "./...",
    ],
    rundefault=[
        "gometalinter.v2",
        "--enable-gc",
        "--deadline=300s",
        "--aggregate",
        "--vendor",
        "--disable=lll",
        "--json",
        "-s",
        "node_modules",
        "-s",
        "src",
        "--config={config_dir}/.gometalinter.json",
        "./...",
    ],
    dotfiles=[".gometalinter.json"],
    language="go",
    autorun=False,
    run_per_file=False,
)
class GometalinterParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for msgdata in json.loads(lint_data):
            try:
                path = msgdata["path"]
                line = msgdata["line"]
                msgbody = msgdata["linter"] + ": " + msgdata["message"]
                messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print("Invalid message: {0}".format(msgdata))
        return messages
