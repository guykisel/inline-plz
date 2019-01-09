# -*- coding: utf-8 -*-

import os.path

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="prettier",
    install=[
        [
            "yarn",
            "add",
            "--dev",
            "prettier",
            "prettier-plugin-java",
        ],
        [
            "npm",
            "install",
            "prettier",
            "prettier-plugin-java",
        ],
        ["npm", "install", "prettier"],
    ],
    help_cmd=[os.path.normpath("./node_modules/.bin/prettier"), "-h"],
    run=[os.path.normpath("./node_modules/.bin/prettier"), "--write"],
    rundefault=[os.path.normpath("./node_modules/.bin/prettier"), "--write"],
    dotfiles=[],
    language="all",
    autorun=False,
    run_per_file=True,
    autofix=True,
)
class PrettierParser(ParserBase):
    """Prettier isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
