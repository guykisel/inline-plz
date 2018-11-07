# -*- coding: utf-8 -*-

import sys

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="black",
    install=[[sys.executable, "-m", "pip", "install", "-U", "black"]],
    help_cmd=["black", "-h"],
    run=["black"],
    rundefault=["black"],
    dotfiles=[],
    language="python",
    autorun=False,
    run_per_file=True,
    autofix=True,
)
class BlackParser(ParserBase):
    """Black isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
