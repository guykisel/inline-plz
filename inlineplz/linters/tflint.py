# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.decorators import linter
from inlineplz.parsers.base import ParserBase
import dirtyjson as json


@linter(
    name = "tflint",
    language = "terraform",
    patterns = ["*.tf"],
    install=[["brew", "install", "tflint"], ["go", "get", "-u", "github.com/wata727/tflint"]],
    help_cmd=["tflint", "--help"],
    run=["tflint", "--format=json"],
    rundefault=["tflint", "--format=json"],
    dotfiles=[],
    autorun=True,
    run_per_file=False,
)
class TFLintParser(ParserBase):
    """Parse tflint output."""

    def parse(self, lint_data):
        messages = set()

        for error_stanza in json.loads(lint_data):
            messages.add(
                (
                    error_stanza.get("file", None),
                    error_stanza.get("line", None),
                    error_stanza.get("message", None),
                )
            )

        return messages
