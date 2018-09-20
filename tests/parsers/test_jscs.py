# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.jscs as jscs

jscs_path = os.path.join("tests", "testdata", "parsers", "jscs.txt")


def test_jscs():
    with codecs.open(jscs_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(jscs.JSCSParser().parse(inputfile.read())))
        assert (
            messages[0][2] == "maximumLineLength: Line must be at most 100 characters"
        )
        assert messages[0][1] == 1
        assert messages[0][0] == "./data/non-ascii-identifier-part-only.js"
