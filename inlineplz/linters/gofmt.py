# -*- coding: utf-8 -*-


from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="gofmt",
    install=[],
    help_cmd=["gofmt", "-h"],
    run=["gofmt", "-w"],
    rundefault=["gofmt", "-w"],
    dotfiles=[],
    language="go",
    autorun=False,
    run_per_file=True,
    autofix=True,
)
class GofmtParser(ParserBase):
    """gofmt isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
