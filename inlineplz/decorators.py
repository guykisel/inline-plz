# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function

from functools import partial
import inspect
from inlineplz.registry import register_linter


LINTERS_BY_NAME = {}
ALL_LINTERS = []


def _create_linter(klass, options):
    kprops = {n: m for (n, m) in inspect.getmembers(klass)}
    config = {
        "name": klass.name,
        "install": kprops.get("install"),
        "help": kprops.get("help"),
        "run": kprops.get("run"),
        "rundefault": kprops.get("rundefault"),
        "dotfiles": kprops.get("dotfiles"),
        "parser": klass,
        "language": kprops.get("language"),
        "patterns": kprops.get("patterns"),
        "autorun": kprops.get("autorun"),
        "run_per_file": kprops.get("run_per_file"),
    }
    register_linter(klass.name, config)
    LINTERS_BY_NAME[klass.name] = config
    ALL_LINTERS.append(klass)
    return klass


def linter(**options):
    return partial(_create_linter, options=options)
