# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os.path

import inlineplz.parsers.markdownlint as markdownlint

markdownlint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'markdownlint.txt'
)


def test_markdownlint():
    with open(markdownlint_path) as inputfile:
        messages = sorted(list(markdownlint.MarkdownLintParser().parse(inputfile.read().decode('utf-8', errors='replace'))))
        assert messages[0][2] == 'MD022 Headers should be surrounded by blank lines'
        assert messages[0][1] == 2
        assert messages[0][0] == './AUTHORS.md'
