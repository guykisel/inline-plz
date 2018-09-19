# -*- coding: utf-8 -*-

import os.path

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="htmlhint",
    install=[["npm", "install", "htmlhint"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/htmlhint"), "-h"],
    run=[os.path.normpath("./node_modules/.bin/htmlhint"), "--format=json"],
    rundefault=[
        os.path.normpath("./node_modules/.bin/htmlhint"),
        "--format=json",
        "--config={config_dir}/.htmlhintrc",
    ],
    dotfiles=[".htmlhintrc"],
    language="html",
    autorun=True,
    run_per_file=False,
)
class HTMLHintParser(ParserBase):
    """Parse json htmlhint output."""

    def parse(self, lint_data):
        messages = set()
        for filedata in json.loads(lint_data):
            if filedata.get("file") and filedata.get("messages"):
                path = filedata["file"]
                for msgdata in filedata["messages"]:
                    try:
                        line = msgdata["line"]
                        msgbody = msgdata["message"]
                        messages.add((path, line, msgbody))
                    except (ValueError, KeyError):
                        print("Invalid message: {0}".format(msgdata))
        return messages
