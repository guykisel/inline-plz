# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.markdownlint as markdownlint

markdownlint_path = os.path.join("tests", "testdata", "parsers", "markdownlint.txt")


def test_markdownlint():
    with codecs.open(
        markdownlint_path, encoding="utf-8", errors="replace"
    ) as inputfile:
        messages = sorted(
            list(markdownlint.MarkdownLintParser().parse(inputfile.read()))
        )
        assert messages[0][2] == "MD022 Headers should be surrounded by blank lines"
        assert messages[0][1] == 2
        assert messages[0][0] == "./AUTHORS.md"
