# -*- coding: utf-8 -*-

import os.path

from ..decorators import linter
from ..parsers.base import ParserBase
from ..util.system import vendored_path


@linter(
    name="pmd",
    install=[],
    help_cmd=[
        vendored_path(os.path.join("pmd", "pmd-bin-6.3.0", "bin", "run.sh")),
        "-help",
    ],
    run=[
        vendored_path(os.path.join("pmd", "pmd-bin-6.3.0", "bin", "run.sh")),
        "pmd",
        "-d",
        ".",
        "-R",
        "java-basic",
        "-f",
        "emacs",
    ],
    rundefault=[
        vendored_path(os.path.join("pmd", "pmd-bin-6.3.0", "bin", "run.sh")),
        "pmd",
        "-d",
        ".",
        "-R",
        "java-basic",
        "-f",
        "emacs",
    ],
    dotfiles=[],
    language="java",
    autorun=True,
    run_per_file=False,
)
class PMDParser(ParserBase):
    """Parse PMD output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.split("\n"):
            try:
                if line.strip():
                    parts = line.split(":")
                    path = parts[0].strip()
                    line_no = int(parts[1].strip())
                    msgbody = parts[2].strip()
                    messages.add((path, line_no, msgbody))
            except (ValueError, IndexError, TypeError):
                print("Invalid message: {0}".format(line))
        return messages
