# -*- coding: utf-8 -*-

import traceback

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="tflint",
    language="terraform",
    patterns=["*.tf"],
    install=[
        ["brew", "tap", "wata727/tflint"],
        ["brew", "install", "tflint"],
        ["go", "get", "-u", "github.com/wata727/tflint"],
    ],
    help_cmd=["tflint", "--help"],
    run=["tflint", "--format=json"],
    rundefault=["tflint", "--format=json"],
    dotfiles=[],
    autorun=True,
    run_per_file=True,
)
class TFLintParser(ParserBase):
    """Parse tflint output."""

    def parse(self, lint_data):
        messages = set()

        for file_path, output in lint_data:
            try:
                for error_stanza in json.loads(output):
                    messages.add(
                        (
                            file_path,
                            error_stanza.get("line", None),
                            error_stanza.get("message", None),
                        )
                    )
            except Exception:
                traceback.print_exc()

        return messages
