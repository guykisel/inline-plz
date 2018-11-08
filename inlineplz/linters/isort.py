# -*- coding: utf-8 -*-

import sys

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="isort",
    install=[[sys.executable, "-m", "pip", "install", "-U", "isort"]],
    help_cmd=["isort", "-h"],
    run=["isort"],
    rundefault=["isort"],
    dotfiles=[],
    language="python",
    autorun=False,
    run_per_file=True,
    autofix=True,
)
class IsortParser(ParserBase):
    """isort isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
