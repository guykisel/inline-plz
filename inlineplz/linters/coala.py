# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import shutil
import sys

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="coala",
    install=[
        ["pipx", "install", "--spec", "coala-bears", "coala"],
        [sys.executable, "-m", "pip", "install", "-U", "coala-bears"],
    ],
    help_cmd=["coala", "-h"],
    run=["coala", "-C", "--json", "--log-json", "--limit-files", "5000"],
    rundefault=["coala", "-C", "--json", "--log-json", "--limit-files", "5000"],
    dotfiles=[".coafile"],
    language="all",
    autorun=True,
    run_per_file=False,
    concurrency=1,
)
class CoalaParser(ParserBase):
    """Parse json coala output."""

    def install(self):
        if not any(
            dotfile.strip() in os.listdir(os.getcwd())
            for dotfile in self.config.get("dotfiles")
        ):
            config_dir = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "config")
            )
            dotfile_name = self.config.get("dotfiles")[0]
            shutil.copyfile(
                os.path.join(config_dir, dotfile_name),
                os.path.join(os.getcwd(), dotfile_name),
            )

    def parse(self, output):
        messages = set()
        lint_data = [
            msg
            for category in json.loads(output).get("results", {}).values()
            for msg in category
        ]
        for msgdata in lint_data:
            try:
                msgbody = msgdata["message"]
                for line in msgdata.get("affected_code", []):
                    path = line.get("file")
                    line = line.get("start", {}).get("line")
                    messages.add((path, line, msgbody))
            except (ValueError, KeyError):
                print("Invalid message: {0}".format(msgdata))
        return messages
