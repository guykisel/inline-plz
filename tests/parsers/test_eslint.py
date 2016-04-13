# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os.path

import inlineplz.parsers.eslint as eslint

eslint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'eslint.txt'
)


def test_eslint():
    with codecs.open(eslint_path, encoding='utf-8', errors='replace') as inputfile:
        messages = sorted(list(eslint.ESLintParser().parse(inputfile.read())))
        assert messages[0][2] == 'Parsing error: Illegal return statement'
        assert messages[0][1] == 17
        assert messages[0][0] == 'C:\\Users\\Guy\\Documents\\jshint\\tests\\unit\\fixtures\\asi.js'
