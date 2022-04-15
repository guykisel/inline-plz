# -*- coding: utf-8 -*-

import re

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="woke",
    language="all",
    patterns=["*.*"],
    install=[["go", "install", "github.com/get-woke/woke@latest"]],
    help_cmd=["woke", "--help"],
    run=["woke"],
    rundefault=["woke"],
    dotfiles=[],
    autorun=True,
    run_per_file=False,
)
class WokeParser(ParserBase):
    """Parse woke output."""

    def parse(self, lint_data):
        messages = set()
        lines = re.compile(r"\n").split(lint_data)
        line_pat = re.compile(r"^(.+?):(\d+):(.+): (.+ \(.+\))")

        for line in lines:
            match = line_pat.search(line)
            if not match:
                continue
            messages.add(
                (
                    match.group(1).strip(),
                    int(match.group(2).strip()),
                    match.group(4).strip(),
                )
            )

        return messages
