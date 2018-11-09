# -*- coding: utf-8 -*-

import os.path

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="eclint",
    install=[["npm", "install", "eclint"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/eclint"), "--help"],
    run=[os.path.normpath("./node_modules/.bin/eclint"), "fix"],
    rundefault=[os.path.normpath("./node_modules/.bin/eclint"), "fix"],
    dotfiles=[],
    language="all",
    autorun=False,
    run_per_file=True,
    run_if_dotfile_in_root=False,
    autofix=True,
)
class ECLintParser(ParserBase):
    """We're running eclint as an autofixer, so no-op."""

    def parse(self, lint_data):
        return []
