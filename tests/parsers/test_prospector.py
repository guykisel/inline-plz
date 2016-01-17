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
        assert messages[0].content == '```\npylint: syntax-error / invalid syntax\n```'
        assert messages[0].line_number == 34
        assert messages[0].path == 'docs/conf.py'
        assert messages[1].content == '```\npylint: unused-import / Unused Message imported from message\n```'
        assert messages[1].line_number == 4
        assert messages[1].path == 'inline-plz/parsers/base.py'
        assert len(messages) == 11
