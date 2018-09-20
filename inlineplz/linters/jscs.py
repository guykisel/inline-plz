# -*- coding: utf-8 -*-

import os.path

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="jscs",
    install=[["npm", "install", "jscs"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/jscs"), "-h"],
    run=[
        os.path.normpath("./node_modules/.bin/jscs"),
        ".",
        "-r",
        "json",
        "-m",
        "-1",
        "-v",
    ],
    rundefault=[
        os.path.normpath("./node_modules/.bin/jscs"),
        ".",
        "-r",
        "json",
        "-m",
        "-1",
        "-v",
        "-c",
        "{config_dir}/.jscsrc",
    ],
    dotfiles=[".jscsrc", ".jscs.json"],
    language="javascript",
    autorun=False,
    run_per_file=False,
)
class JSCSParser(ParserBase):
    """Parse json jscs output."""

    def parse(self, lint_data):
        messages = set()
        for filename, msgs in json.loads(lint_data).items():
            if msgs:
                for msgdata in msgs:
                    try:
                        path = filename
                        line = msgdata["line"]
                        msgbody = msgdata["message"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print("Invalid message: {0}".format(msgdata))
        return messages
