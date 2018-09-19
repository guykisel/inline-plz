# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.gometalinter as gometalinter

eslint_path = os.path.join("tests", "testdata", "parsers", "gometalinter.txt")


def test_gometalinter():
    with codecs.open(eslint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(
            list(gometalinter.GometalinterParser().parse(inputfile.read()))
        )
        assert (
            messages[0][2]
            == "golint: exported type Severity should have comment or be unexported"
        )
        assert messages[0][1] == 23
        assert messages[0][0] == "main.go"
