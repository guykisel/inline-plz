# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

import inlineplz.parsers.jscs as jscs

jscs_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'jscs.txt'
)


def test_jscs():
    with open(jscs_path) as inputfile:
        messages = jscs.JSCSParser().parse(inputfile.read())
        assert messages[0].content == '`maximumLineLength: Line must be at most 100 characters`'
        assert messages[0].line_number == 1
        assert messages[0].path == 'data/non-ascii-identifier-part-only.js'
