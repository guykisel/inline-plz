# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os

import inlineplz.parsers.stylint as stylint


stylint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'stylint.txt'
)


def test_stylint():
    with codecs.open(stylint_path, encoding='utf-8', errors='replace') as inputfile:
        messages = sorted(list(stylint.StylintParser().parse(inputfile.read())))
        assert messages[0][2] == "Warning: preferred quote style is single quotes"
        assert messages[0][1] == 11
        assert messages[0][0] == './test-styl/_ads.styl'
