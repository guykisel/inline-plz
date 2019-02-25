# -*- coding: utf-8 -*-

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="golangci-lint",
    install=[
        ["go", "get", "-u", "github.com/golangci/golangci-lint/cmd/golangci-lint"]
    ],
    help_cmd=["golangci-lint", "--help"],
    run=[
        "golangci-lint",
        "run",
        "--out-format",
        "json",
        "--max-issues-per-linter",
        "0",
        "--max-same-issues",
        "0",
    ],
    rundefault=[
        "golangci-lint",
        "run",
        "--config",
        "{config_dir}/.golangci.yml",
        "--out-format",
        "json",
    ],
    dotfiles=[".golangci.yml", ".golangci.toml", ".golangci.json"],
    language="go",
    autorun=False,
    run_per_file=False,
)
class GolangcilintParser(ParserBase):
    """Parse json golangci-lint output."""

    def parse(self, lint_data):
        messages = set()
        for msgdata in json.loads(lint_data).get("Issues", []):
            try:
                path = msgdata["Pos"]["Filename"]
                line = msgdata["Pos"]["Line"]
                msgbody = msgdata["FromLinter"] + ": " + msgdata["Text"]
                messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print("Invalid message: {0}".format(msgdata))
        return messages
