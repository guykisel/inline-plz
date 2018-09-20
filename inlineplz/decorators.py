# -*- coding: utf-8 -*-


from functools import partial

from .registry import register_linter

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


def linter(
    name,
    install,
    help_cmd,
    run,
    rundefault,
    dotfiles,
    language,
    autorun,
    run_per_file,
    concurrency=None,
    run_if_dotfile_in_root=None,
    patterns=None,
    url=None,
):
    return partial(
        _create_linter,
        config={
            "name": name,
            "install": install,
            "help_cmd": help_cmd,
            "run": run,
            "rundefault": rundefault,
            "dotfiles": dotfiles,
            "language": language,
            "autorun": autorun,
            "run_per_file": run_per_file,
            "concurrency": concurrency,
            "run_if_dotfile_in_root": run_if_dotfile_in_root,
            "patterns": patterns,
            "url": url,
        },
    )
