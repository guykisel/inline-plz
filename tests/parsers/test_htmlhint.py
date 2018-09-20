# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.htmlhint as htmlhint

htmlhint_path = os.path.join("tests", "testdata", "parsers", "htmlhint.txt")


def test_htmlhint():
    with codecs.open(htmlhint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(htmlhint.HTMLHintParser().parse(inputfile.read())))
        assert messages[0][0] == "./data/executable.html"
        assert messages[0][1] == 8
        assert messages[0][2] == "Duplicate of attribute name [ bad ] was found."
