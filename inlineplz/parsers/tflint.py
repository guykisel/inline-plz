# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import re

from inlineplz.parsers.base import ParserBase


class TFLintParser(ParserBase):
    """Parse tflint output."""

    def rematch(self, string, regex):
        self.re_last_string = string
        self.re_last_regex = regex

        # TODO cache / memoize compilation of the regexes
        if type(regex) == str:
            regex = re.compile(regex)

        m = re.search(regex, string)
        self.re_last_m = m
        return m


    def string_to_lines(self, s):
        # TODO: cache the compiled regex7
       return re.compile("\\r?\\n").split(s)

    def parse(self, lint_data):
        messages = set()
        # NB: tflint doesn't seem to emit a line number :(

        # 01-testcase.tf
        # 	ERROR:7 "ms1.2xlarge" is invalid instance type. (aws_instance_invalid_type)
        # 	ERROR:7 "ms1.2xlarge" is invalid instance type. (aws_instance_invalid_type) #
        # Result: 2 issues  (2 errors , 0 warnings , 0 notices)
        #
        current_file = None
        lines = self.string_to_lines(lint_data)
        while lines:
            lint_output_line = lines.pop(0).strip()
            # print(u"LINE={}".format(lint_output_line))

            if self.rematch(lint_output_line, "^Result:"):
                continue

            if self.rematch(lint_output_line, "^(\\S+)$"):
                current_file = self.re_last_m.groups()[0]
                continue

            if self.rematch(lint_output_line, "^$"):
                current_file = None
                continue

            if not current_file:
                raise ValueError(u"Error: unrecognized tflint output, unable to determine filename at line=''".format(lint_output_line))
            messages.add((current_file, -1, lint_output_line))

        return messages
