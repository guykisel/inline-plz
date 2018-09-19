# -*- coding: utf-8 -*-

import inlineplz.linters.jsonlint as jsonlint


def test_jsonlint():
    input = [
        ("21.json", "21.json: line 1, col 25, found: ',' - expected: ':'."),
        (
            "25.json",
            "25.json: line 1, col 1, found: 'INVALID' - expected: 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '[', ']'.",
        ),
        (
            "23.json",
            "23.json: line 1, col 13, found: 'INVALID' - expected: 'STRING', 'NUMBER', 'NULL', 'TRUE', 'FALSE', '{', '['.",
        ),
    ]
    messages = sorted(list(jsonlint.JSONLintParser().parse(input)))
    assert messages[0][2] == "21.json: line 1, col 25, found: ',' - expected: ':'."
    assert messages[0][1] == 1
    assert messages[0][0] == "21.json"
