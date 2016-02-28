# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

import inlineplz.linters as linters


def test_rundefault_config():
    test_config = {
        'run': ['run'],
        'rundefault': ['rundefault'],
        'dotfiles': []
    }
    test_config_path = os.path.join(
        os.getcwd(), 'tests',
        'testdata', 'linter_configs'
    )
    assert linters.run_config(test_config, test_config_path) == ['rundefault']


def test_run_config():
    test_config = {
        'run': ['run'],
        'rundefault': ['rundefault'],
        'dotfiles': ['.dotfile']
    }
    test_config_path = os.path.join(
        os.getcwd(), 'tests',
        'testdata', 'linter_configs'
    )
    assert linters.run_config(test_config, test_config_path) == ['rundefault']
