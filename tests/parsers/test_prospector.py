# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.prospector as prospector

prospector_path = os.path.join("tests", "testdata", "parsers", "prospector.txt")


def test_prospector():
    with codecs.open(prospector_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(prospector.ProspectorParser().parse(inputfile.read())))
        assert messages[0][2] == "pep257: Missing docstring in public package (D104)"
        assert messages[0][1] == 1
        assert messages[0][0] == "inlineplz\__init__.py"

        assert messages[1][2] == "pep257: Missing docstring in public package (D104)"
        assert messages[1][1] == 1
        assert messages[1][0] == "inlineplz\interfaces\__init__.py"

        assert messages[9][2] == "pep257: Missing docstring in public package (D104)"
        assert messages[9][1] == 1
        assert len(messages) == 32
