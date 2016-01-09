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
        assert messages
