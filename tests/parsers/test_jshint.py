# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

import inlineplz.parsers.jshint as jshint

jshint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'jshint.txt'
)


def test_jshint():
    with open(jshint_path) as inputfile:
        messages = jshint.JSHintParser().parse(inputfile.read())
        assert messages[0].content == '`Use the function form of "use strict". (W097)`'
        assert messages[0].line_number == 8
        assert messages[0].path == 'conf/cli-options.js'
