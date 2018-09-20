# -*- coding: utf-8 -*-

import sys

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="bandit",
    install=[[sys.executable, "-m", "pip", "install", "-U", "bandit"]],
    help_cmd=["bandit", "-h"],
    run=["bandit", "-f", "json", "-iii", "-ll", "-r", "."],
    rundefault=[
        "bandit",
        "-f",
        "json",
        "-iii",
        "-ll",
        "-r",
        ".",
        "-c",
        "{config_dir}/bandit.yaml",
    ],
    dotfiles=["bandit.yaml"],
    language="python",
    autorun=True,
    run_per_file=False,
)
class BanditParser(ParserBase):
    """Parse json bandit output."""

    def parse(self, lint_data):
        messages = set()
        lint_data_lines = lint_data.split("\n")
        # bandit spits out some unwanted debug messages before the json
        for line in lint_data_lines[:]:
            if line.strip().startswith("[main]"):
                lint_data_lines.remove(line)
        lint_data_cleaned = "\n".join(lint_data_lines).strip()
        for msgdata in json.loads(lint_data_cleaned).get("results"):
            try:
                path = msgdata["filename"]
                line = msgdata["line_number"]
                msgbody = msgdata["issue_text"]
                messages.add((path.strip(), line, msgbody.strip()))
            except (ValueError, KeyError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, msgdata))
        return messages
