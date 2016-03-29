# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os.path

import inlineplz.parsers.rflint as rflint

rflint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'rflint.txt'
)


def test_rflint():
    with open(rflint_path) as inputfile:
        messages = sorted(list(rflint.RobotFrameworkLintParser().parse(inputfile.read())))
        assert messages[-1][2] == 'Too few steps (1) in keyword (TooFewKeywordSteps)'
        assert messages[-1][1] == 30
        assert messages[-1][0] == './Functional_Requirements/keywords.robot'
