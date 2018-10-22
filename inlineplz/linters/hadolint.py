# -*- coding: utf-8 -*-

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="hadolint",
    install=[
        ["cabal", "update"],
        ["cabal", "install", "hadolint"],
        ["apt-get", "install", "hadolint"],
        ["dnf", "install", "hadolint"],
        ["brew", "install", "hadolint"],
        ["port", "install", "hadolint"],
        ["zypper", "in", "hadolint"],
    ],
    help_cmd=["hadolint", "--help"],
    run=["hadolint", "-f", "json"],
    rundefault=["hadolint", "-f", "json"],
    dotfiles=[],
    language="docker",
    autorun=True,
    run_per_file=True,
)
class HadolintParser(ParserBase):
    """Parse json hadolint output."""

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
                            msgbody = msgdata["code"] + ": " + msgdata["message"]
                            messages.add((path, line, msgbody))
                        except (ValueError, KeyError, TypeError):
                            print(
                                "({0}) Invalid message: {1}".format(
                                    type(self).__name__, msgdata
                                )
                            )
        return messages
