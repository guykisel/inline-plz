# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import traceback

import sys
import dirtyjson as json

from inlineplz.parsers.base import ParserBase
from inlineplz.decorators import linter


@linter(
    name="prospector",
    install=[
        [sys.executable, "-m", "pip", "install", "-U", "prospector[with_everything]"],
        [sys.executable, "-m", "pip", "install", "-U", "prospector"],
    ],
    help_cmd=["prospector", "-h"],
    run=["prospector", "--zero-exit", "-o", "json"],
    rundefault=[
        "prospector",
        "--zero-exit",
        "-o",
        "json",
        "-P",
        "{config_dir}/.prospector.yaml",
    ],
    dotfiles=[".prospector.yaml"],
    language="python",
    autorun=True,
    run_per_file=False,
)
class ProspectorParser(ParserBase):
    """Parse json prospector output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for msgdata in json.loads(lint_data).get("messages"):
                try:
                    path = msgdata["location"]["path"]
                    line = msgdata["location"]["line"]
                    msgbody = "{0}: {1} ({2})".format(
                        msgdata["source"], msgdata["message"], msgdata["code"]
                    )
                    messages.add((path, line, msgbody))
                except (ValueError, KeyError):
                    print("({0}) Invalid message: {1}".format(type(self).__name__, msgdata))
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
