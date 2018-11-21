# -*- coding: utf-8 -*-

# import dirtyjson as json
import json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="clippy",
    install=[["rustup", "component", "add", "clippy-preview"]],
    help_cmd=["cargo", "clippy", "--help"],
    run=[
        "cargo",
        "clippy",
        "--quiet",
        "--message-format=json",
        "--all",
        "--bins",
        "--tests",
        "--examples",
        "--benches",
    ],
    rundefault=[
        "cargo",
        "clippy",
        "--quiet",
        "--message-format=json",
        "--all",
        "--bins",
        "--tests",
        "--examples",
        "--benches",
    ],
    dotfiles=[],
    language="rust",
    autorun=True,
    run_per_file=False,
)
class ClippyParser(ParserBase):
    """Parse json clippy output."""

    def parse(self, lint_data):
        messages = set()
        for line in lint_data.splitlines():
            message = json.loads(line)
            try:
                if "message" in message:
                    messages.add(
                        (
                            message["message"]["spans"][0]["file_name"],
                            int(message["message"]["spans"][0]["line_start"]),
                            message["message"]["rendered"],
                        )
                    )
            except (ValueError, KeyError):
                print("Invalid message: {0}".format(json.dumps(message)))
        return messages
