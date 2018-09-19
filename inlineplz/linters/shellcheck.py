# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="shellcheck",
    install=[
        ["cabal", "update"],
        ["cabal", "install", "shellcheck"],
        ["apt-get", "install", "shellcheck"],
        ["dnf", "install", "shellcheck"],
        ["brew", "install", "shellcheck"],
        ["port", "install", "shellcheck"],
        ["zypper", "in", "ShellCheck"],
    ],
    help_cmd=["shellcheck", "-V"],
    run=["shellcheck", "-f", "json"],
    rundefault=["shellcheck", "-f", "json"],
    dotfiles=[],
    language="shell",
    autorun=True,
    run_per_file=True,
)
class ShellcheckParser(ParserBase):
    """Parse json shellcheck output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            if file_path.strip() and output.strip():
                filedata = json.loads(output)
                if filedata:
                    for msgdata in filedata:
                        try:
                            path = file_path
                            line = msgdata["line"]
                            msgbody = msgdata["message"]
                            messages.add((path, line, msgbody))
                        except (ValueError, KeyError, TypeError):
                            print("({0}) Invalid message: {1}".format(type(self).__name__, msgdata))
        return messages
