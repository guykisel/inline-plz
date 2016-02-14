# -*- coding: utf-8 -*-

from __future__ import absolute_import

from inlineplz.parsers.prospector import ProspectorParser
from inlineplz.parsers.eslint import ESLintParser
from inlineplz.parsers.jscs import JSCSParser
from inlineplz.parsers.jshint import JSHintParser
from inlineplz.parsers.jsonlint import JSONLintParser
from inlineplz.parsers.yamllint import YAMLLintParser


PARSERS = {
    'prospector': ProspectorParser,
    'eslint': ESLintParser,
    'jshint': JSHintParser,
    'jscs': JSCSParser,
    'jsonlint': JSONLintParser,
    'yamllint': YAMLLintParser
}
