# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.gherkinlint as gherkinlint

gherkinlint_path = os.path.join("tests", "testdata", "parsers", "gherkin-lint.txt")


def test_gherkinlint():
    with codecs.open(gherkinlint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(gherkinlint.GherkinLintParser().parse(inputfile.read())))
        print(messages)
        assert (
            messages[0][2] == "Feature name is already used in: features/fake.feature"
        )
        assert messages[0][1] == 1
        assert messages[0][0] == "D:\\Git\\vsiakka\\features\\test3.feature"
