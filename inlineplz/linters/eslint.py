# -*- coding: utf-8 -*-

import os.path

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="eslint",
    install=[["npm", "install", "eslint"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/eslint"), "-h"],
    run=[os.path.normpath("./node_modules/.bin/eslint"), ".", "-f", "unix"],
    rundefault=[
        os.path.normpath("./node_modules/.bin/eslint"),
        ".",
        "-f",
        "unix",
        "-c",
        "{config_dir}/.eslintrc.js",
        "--ignore-path",
        "{config_dir}/.eslintignore",
    ],
    dotfiles=[
        ".eslintrc.yml",
        ".eslintrc.yaml",
        ".eslintignore",
        ".eslintrc",
        ".eslintrc.js",
        ".eslintrc.json",
    ],
    language="javascript",
    autorun=True,
    run_per_file=False,
)
class ESLintParser(ParserBase):
    """Parse json eslint output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split("\n"):
            try:
                parts = line.split(":")
                if line.strip() and parts:
                    path = parts[0].strip()
                    line = int(parts[1].strip())
                    msgbody = ":".join(parts[3:]).strip()
                    messages.add((path, line, msgbody))
            except (ValueError, IndexError):
                print("Invalid message: {0}".format(line))
        return messages
