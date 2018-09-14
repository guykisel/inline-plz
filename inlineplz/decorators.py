# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from functools import partial
import inspect
from inlineplz.registry import register_linter


LINTERS_BY_NAME = {}
ALL_LINTERS = []


def _create_linter(klass, config):
    if "name" not in config:
        config["name"] = klass.__class__.__name__
    config["parser"] = klass
    register_linter(config["name"], config)
    LINTERS_BY_NAME[config["name"]] = config
    ALL_LINTERS.append(klass)
    return klass


def linter(config):
    return partial(_create_linter, config=config)
