
import os.path
import traceback

import dirtyjson as json

from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="gherkin-lint",
    install=[["npm", "install", "gherkin-lint"]],
    help_cmd=[os.path.normpath("./node_modules/.bin/gherkin-lint"), "--help"],
    run=[os.path.normpath("./node_modules/.bin/gherkin-lint"), ".", "-f", "json"],
    rundefault=[
        os.path.normpath("./node_modules/.bin/gherkin-lint"),
        ".",
        "-f",
        "json",
        "-c",
        "{config_dir}/.gherkin-lintrc",
    ],
    dotfiles=[".gherkin-lintrc"],
    language="gherkin",
    autorun=True,
    run_per_file=False,
)
class GherkinLintParser(ParserBase):
    """Parse json gherkin-lint output."""

    def parse(self, lint_data):
        messages = set()
        try:
            for filedata in json.loads(lint_data):
                if filedata.get("errors") and filedata.get("filePath"):
                    path = filedata["filePath"]
                    for msgdata in filedata["errors"]:
                        try:
                            line = msgdata["line"]
                            msgbody = msgdata["message"]
                            messages.add((path, line, msgbody))
                        except (ValueError, KeyError):
                            print(
                                "({0}) Invalid message: {1}".format(
                                    type(self).__name__, msgdata
                                )
                            )
        except ValueError:
            print(traceback.format_exc())
            print(lint_data)
        return messages
