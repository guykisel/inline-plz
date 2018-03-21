# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import codecs
import os

import inlineplz.parsers.yamllint as yamllint


yamllint_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'yamllint.txt'
)

def test_yamllint():
    with codecs.open(yamllint_path, encoding='utf-8', errors='replace') as inputfile:
        messages = sorted(list(yamllint.YAMLLintParser().parse(inputfile.read())))
        assert messages[0][2] == '[warning] missing document start "---" (document-start)'
        assert messages[0][1] == 1
        assert messages[0][0] == '.\.inlineplz.yml'
