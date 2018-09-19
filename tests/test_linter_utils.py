# -*- coding: utf-8 -*-
import os

from inlineplz.linter_runner import LinterRunner


def test_no_dotfile_config():
    test_config = {"run": ["run"], "rundefault": ["rundefault"], "dotfiles": []}
    linter_runner = LinterRunner(
        config_dir=os.path.join(os.getcwd(), "tests", "testdata", "linter_configs")
    )
    assert linter_runner.run_config(test_config) == ["run"]


def test_rundefault_config():
    test_config = {
        "run": ["run"],
        "rundefault": ["rundefault"],
        "dotfiles": [".dotfile"],
    }
    linter_runner = LinterRunner(
        config_dir=os.path.join(os.getcwd(), "tests", "testdata", "linter_configs")
    )
    assert linter_runner.run_config(test_config) == ["rundefault"]


def test_dotfiles_dont_exist():
    test_config = {
        "run": ["run"],
        "rundefault": ["rundefault"],
        "dotfiles": [".dotfile_doesnt_exist"],
    }
    assert not LinterRunner.dotfiles_exist(
        test_config, os.path.join(os.getcwd(), "tests", "testdata", "linter_configs")
    )


def test_dotfiles_exist():
    test_config = {
        "run": ["run"],
        "rundefault": ["rundefault"],
        "dotfiles": [".dotfile"],
    }
    assert LinterRunner.dotfiles_exist(
        test_config, os.path.join(os.getcwd(), "tests", "testdata", "linter_configs")
    )
