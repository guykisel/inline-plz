# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

import inlineplz.parsers.eslint as eslint

eslint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'eslint.txt'
)


def test_eslint():
    with open(eslint_path) as inputfile:
        messages = eslint.ESLintParser().parse(inputfile.read())
        assert messages[0].content == '`Parsing error: Illegal return statement`'
        assert messages[0].line_number == 17
        assert messages[0].path == 'C:/Users/Guy/Documents/jshint/tests/unit/fixtures/asi.js'
