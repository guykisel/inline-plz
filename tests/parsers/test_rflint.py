# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.rflint as rflint

rflint_path = os.path.join("tests", "testdata", "parsers", "rflint.txt")


def test_rflint():
    with codecs.open(rflint_path, encoding="utf-8", errors="replace") as inputfile:
        test_data = inputfile.readlines()
        test_filename = ""
        test_input = []
        for line in test_data:
            if line.startswith("+"):
                test_filename = line.split(" ")[-1].strip()
            test_input.append((test_filename, line))
    messages = sorted(list(rflint.RobotFrameworkLintParser().parse(test_input)))
    assert messages[-1][2] == "Too few steps (1) in keyword (TooFewKeywordSteps)"
    assert messages[-1][1] == 30
    assert messages[-1][0] == "./Functional_Requirements/keywords.robot"
