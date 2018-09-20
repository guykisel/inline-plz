# -*- coding: utf-8 -*-

import codecs
import os

import inlineplz.linters.tflint as tflint

tflint_path = os.path.join(
    "tests", "testdata", "parsers", "tflint.01-testcase.tf.stdout"
)


def test_tflint():
    with codecs.open(tflint_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(
            list(tflint.TFLintParser().parse([("01-testcase.tf", inputfile.read())]))
        )
        expected = sorted(
            [
                ("01-testcase.tf", 7, '"ms1.2xlarge" is invalid instance type.'),
                ("01-testcase.tf", 7, '"ms2000.2xlarge" is invalid instance type.'),
            ]
        )

        lmessages = len(messages)
        lexpected = len(expected)
        assert lmessages == lexpected
        for (tactual, texpected) in zip(messages, expected):
            assert tactual == texpected
