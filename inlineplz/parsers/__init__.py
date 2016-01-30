# -*- coding: utf-8 -*-

from __future__ import absolute_import

from inlineplz.parsers.prospector import ProspectorParser
from inlineplz.parsers.eslint import ESLintParser
from inlineplz.parsers.jscs import JSCSParser
from inlineplz.parsers.jshint import JSHintParser
from inlineplz.parsers.jslint import JSLintParser


PARSERS = {
    'prospector': ProspectorParser,
    'eslint': ESLintParser,
    'jshint': JSHintParser,
    'jscs': JSCSParser,
    'jslint': JSLintParser
}
