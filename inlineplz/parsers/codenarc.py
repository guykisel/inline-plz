# -*- coding: utf-8 -*-

from ..parsers.base import ParserBase


class CodenarcParser(ParserBase):
    """Parse Codenarc output."""

    def parse(self, lint_data):
        messages = set()
        path = ""
        msg = ""
        line_no = -1
        for line in lint_data.split("\n"):
            try:
                if line.strip().startswith("File:"):
                    path = line.split("File:")[-1].strip()
                    continue

                if line.strip().startswith("Violation:"):
                    parts = line.strip().split()
                    line_no = int(parts[3].split("=")[-1])
                    msg = line.strip()
                else:
                    msg += "\n" + line
                if "Src=" in line:
                    messages.add((path, line_no, msg))
                    msg = ""
            except (ValueError, IndexError, TypeError):
                print("({0}) Invalid message: {1}".format(type(self).__name__, line))
        return messages
