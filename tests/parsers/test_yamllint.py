# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import inlineplz.parsers.yamllint as yamllint


def test_yamllint():
    input = [
        ('.travis.yml', "File : .travis.yml, error: (.travis.yml): mapping values are not allowed in this context at line 2 column 6")
    ]
    messages = sorted(list(yamllint.YAMLLintParser().parse(input)))
    assert messages[0][2] == "File : .travis.yml, error: (.travis.yml): mapping values are not allowed in this context at line 2 column 6"
    assert messages[0][1] == 2
    assert messages[0][0] == '.travis.yml'
