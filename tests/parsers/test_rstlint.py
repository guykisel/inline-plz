# -*- coding: utf-8 -*-

import inlineplz.linters.rstlint as rstlint


def test_rstlint():
    input = [
        (
            "README.rst",
            '[{"message": "Document or section may not begin with a transition.", "full_message": "Document or section may not begin with a transition.", "source": "README.rst", "type": "ERROR", "level": 3, "line": 4}]',
        )
    ]
    messages = sorted(list(rstlint.RSTLintParser().parse(input)))
    assert messages[0][2] == "Document or section may not begin with a transition."
    assert messages[0][1] == 4
    assert messages[0][0] == "README.rst"
