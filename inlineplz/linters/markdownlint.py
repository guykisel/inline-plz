# -*- coding: utf-8 -*-

import os.path

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="markdownlint-cli",
    install=[["npm", "install", "markdownlint-cli"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/markdownlint"), "-h"],
    run=[os.path.normpath("./node_modules/.bin/markdownlint"), "."],
    rundefault=[
        os.path.normpath("./node_modules/.bin/markdownlint"),
        ".",
        "-c",
        "{config_dir}/.markdownlintrc",
    ],
    dotfiles=[".markdownlintrc", ".markdownlint.json"],
    language="markdown",
    autorun=True,
    run_per_file=False,
)
class MarkdownLintParser(ParserBase):
    """Parse markdownlint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split("\n"):
            try:
                parts = line.split(":")
                if line.strip() and parts:
                    path = parts[0].strip()
                    line = int(parts[1].strip())
                    msgbody = ":".join(parts[2:]).strip()
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, line))
        return messages
