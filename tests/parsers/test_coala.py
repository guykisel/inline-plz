# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.coala as coala

coala_path = os.path.join("tests", "testdata", "parsers", "coala.txt")


def test_coala():
    with codecs.open(coala_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(coala.CoalaParser().parse(inputfile.read())))
        assert messages[0][0] == "./data/test.c"
        assert messages[0][1] == 1
        assert messages[0][2] == "Line is longer than allowed. (98 > 79)"
