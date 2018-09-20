# -*- coding: utf-8 -*-

import os.path

import xmltodict

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="jshint",
    install=[["npm", "install", "jshint"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/jshint"), "-h"],
    run=[
        os.path.normpath("./node_modules/.bin/jshint"),
        ".",
        "--reporter",
        "checkstyle",
    ],
    rundefault=[
        os.path.normpath("./node_modules/.bin/jshint"),
        ".",
        "--reporter",
        "checkstyle",
        "-c",
        "{config_dir}/.jshintrc",
    ],
    dotfiles=[".jshintrc"],
    language="javascript",
    autorun=False,
    run_per_file=False,
)
class JSHintParser(ParserBase):
    """Parse json jshint output."""

    def parse(self, lint_data):
        messages = set()
        obj = xmltodict.parse(lint_data)
        if "file" in obj["checkstyle"]:
            # handle single file
            try:
                path = obj["checkstyle"]["file"]["@name"]
                # handle single error
                try:
                    create_message_from_error(
                        messages, path, obj["checkstyle"]["file"]["error"]
                    )
                except TypeError:
                    for errordata in obj["checkstyle"]["file"]["error"]:
                        create_message_from_error(messages, path, errordata)
            # handle many files
            except TypeError:
                for filedata in obj["checkstyle"]["file"]:
                    path = filedata["@name"]
                    # handle single error
                    try:
                        create_message_from_error(messages, path, filedata["error"])
                    except TypeError:
                        for errordata in filedata["error"]:
                            try:
                                create_message_from_error(messages, path, errordata)
                            except (AttributeError, TypeError):
                                pass
        return messages


def create_message_from_error(messages, path, errordata):
    line = int(errordata["@line"])
    msgbody = errordata["@message"]
    messages.add((path, line, msgbody))
