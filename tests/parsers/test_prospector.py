# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import os.path

import pytest

import inlineplz.parsers.prospector as prospector

prospector_path = os.path.join(
    'tests',
    'testdata',
    'parsers',
    'prospector.txt'
)


def test_prospector():
    with open(prospector_path) as inputfile:
        messages = sorted(list(prospector.ProspectorParser().parse(inputfile.read().decode('utf-8', errors='replace'))))
        assert messages[0][2] == 'pep257: Missing docstring in public package (D104)'
        assert messages[0][1] == 1
        assert messages[0][0] == 'inlineplz\__init__.py'

        assert messages[1][2] == 'pep257: Missing docstring in public package (D104)'
        assert messages[1][1] == 1
        assert messages[1][0] == 'inlineplz\interfaces\__init__.py'

        assert messages[9][2] == 'pep257: Missing docstring in public package (D104)'
        assert messages[9][1] == 1
        assert len(messages) == 32
