# -*- coding: utf-8 -*-

import re

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="todolint",
    url="https://bitbucket.org/atlassian/todolint",
    language="all",
    patterns=["*.*"],
    install=[["go", "get", "-u", "bitbucket.org/atlassian/todolint"]],
    help_cmd=["todolint", "--help"],
    run=["todolint"],
    rundefault=["todolint"],
    dotfiles=[],
    autorun=True,
    run_per_file=False,
)
class TodoLintParser(ParserBase):
    """Parse todolint output."""

    def parse(self, lint_data):
        messages = set()
        lines = re.compile(r"\r?\n").split(lint_data)
        line_pat = re.compile(r"^(.+?) \((\d+)\): (.+)$")

        for line in lines:
            match = line_pat.search(line)
            if not match:
                continue
            messages.add(
                (
                    match.group(1).strip(),
                    int(match.group(2).strip()),
                    match.group(3).strip(),
                )
            )

        return messages
