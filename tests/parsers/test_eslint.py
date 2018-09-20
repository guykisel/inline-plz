# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.eslint as eslint

eslint_path = os.path.join("tests", "testdata", "parsers", "eslint.txt")


def test_eslint():
    with codecs.open(eslint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(eslint.ESLintParser().parse(inputfile.read())))
        assert (
            messages[0][2]
            == "'addOne' is defined but never used. [Error/no-unused-vars]"
        )
        assert messages[0][1] == 1
        assert (
            messages[0][0]
            == "/var/lib/jenkins/workspace/Releases/ESLint Release/eslint/fullOfProblems.js"
        )
