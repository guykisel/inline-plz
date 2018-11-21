# -*- coding: utf-8 -*-


from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="sh",
    install=[["go", "get", "-u", "mvdan.cc/sh/cmd/shfmt"]],
    help_cmd=["shfmt", "-h"],
    run=["shfmt", "-w", "-s"],
    rundefault=["shfmt", "-w", "-s"],
    dotfiles=[],
    language="shell",
    autorun=False,
    run_per_file=True,
    autofix=True,
)
class ShfmtParser(ParserBase):
    """shfmt isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
