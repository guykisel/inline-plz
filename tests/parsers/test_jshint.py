# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os.path

import inlineplz.parsers.jshint as jshint

jshint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'jshint.txt'
)


def test_jshint():
    with codecs.open(jshint_path, encoding='utf-8', errors='replace') as inputfile:
        messages = sorted(list(jshint.JSHintParser().parse(inputfile.read())))
        assert messages[0][2] == 'Use the function form of "use strict". (W097)'
        assert messages[0][1] == 7
        assert messages[0][0] == 'Makefile.js'
