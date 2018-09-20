# -*- coding: utf-8 -*-

# glob patterns for what language is represented by what type of files.
PATTERNS = {}
# linter configs. add new tools here.
LINTERS = {}


def register_pattern(pname, patterns):
    if pname in PATTERNS:
        print(u"WARNING: duplicate pattern: {}".format(pname))
    PATTERNS[pname] = patterns


def get_patterns():
    return PATTERNS


def register_linter(lname, options):
    if lname in LINTERS:
        print(u"WARNING: duplicate pattern: {}".format(lname))

    LINTERS[lname] = options
    patterns = options.get("patterns", None)
    if patterns:
        register_pattern(options["language"], patterns)


def get_linters():
    return LINTERS
