# -*- coding: utf-8 -*-

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
        messages = prospector.ProspectorParser().parse(inputfile.read())
        #print([msg.content for msg in messages])
        assert messages[0].content == '`pep257: Missing docstring in public package (D104)`'
        assert messages[0].line_number == 1
        assert messages[0].path == 'inlineplz/util/__init__.py'
        assert messages[1].content == '`pep257: Missing docstring in public package (D104)`'
        assert messages[1].line_number == 1
        assert messages[1].path == 'inlineplz/parsers/__init__.py'
        assert messages[9].content == ('`pep257: One-line docstring should fit on one line with quotes (found 2) (D200)`')
        assert messages[9].line_number == 1
        assert len(messages) == 32
