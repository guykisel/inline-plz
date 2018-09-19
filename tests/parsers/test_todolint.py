# -*- coding: utf-8 -*-

import codecs
import os

import inlineplz.linters.todolint as todolint

todolint_path = os.path.join("tests", "testdata", "parsers", "todolint.stdout")


def test_todolint():
    with codecs.open(todolint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(todolint.TodoLintParser().parse(inputfile.read())))
        expected = sorted(
            [
                ("setup.py", 27, "# TODO: put package test requirements here"),
                (
                    "inlineplz/main.py",
                    158,
                    "# TODO: consider moving this git parsing stuff into the github interface",
                ),
                (
                    "inlineplz/main.py",
                    227,
                    "# TODO: implement dryrun as an interface instead of a special case here",
                ),
                # inlineplz/interfaces/github.py (94):         # TODO: support  non-PR runs
                ("inlineplz/interfaces/github.py", 94, "# TODO: support non-PR runs"),
                (
                    "inlineplz/linters/__init__.py",
                    109,
                    '# TODO: can we not do this at "compile" or "import" time?',
                ),
                (
                    "inlineplz/linters/detectsecrets.py",
                    15,
                    "# TODO: switch this to installing from pypi once they release my fix from https://github.com/Yelp/detect-secrets/pull/69",
                ),
                ("node_modules/agent-base/index.js", 168, "// TODO reuse sockets"),
                ("node_modules/dashdash/README.md", 275, "- TODO: document specExtra"),
                (
                    "node_modules/dashdash/README.md",
                    276,
                    "- TODO: document includeHidden",
                ),
                (
                    "node_modules/dashdash/README.md",
                    277,
                    "- TODO: document custom types, `function complete\_FOO` guide, completionType",
                ),
                ("node_modules/dashdash/README.md", 278, "- TODO: document argtypes"),
                (
                    "node_modules/eslint-utils/index.js",
                    460,
                    "// TODO(mysticatea): don't support destructuring here.",
                ),
            ]
        )

        lmessages = len(messages)
        lexpected = len(expected)
        assert lmessages == lexpected
        for (tactual, texpected) in zip(messages, expected):
            assert tactual == texpected
