# -*- coding: utf-8 -*-

"""Wrap linter messages in a generic Message class that can do some internal cleanup."""


import os
import traceback


class Messages:
    def __init__(self):
        self.messages = {}

    def add_message(self, path, line, message):
        path = os.path.relpath(path).replace("\\", "/").strip()
        # replace backticks with single quotes to avoid markdown escaping issues
        message = message.replace("`", "'").strip()
        try:
            line = int(line)
        except (ValueError, TypeError):
            line = 1
        if line <= 0:
            line = 1
        # replace line numbers to improve deduping. we're commenting inline anyway,
        # so line numbers don't really matter
        if line > 1:
            message = message.replace(str(line), "_")
        if (path, line) not in self.messages:
            try:
                self.messages[(path, line)] = Message(path, line)
            except TypeError:
                print("{0} {1} {2}".format(path, line, message))
                print(traceback.format_exc())
                return

        self.messages[(path, line)].append(message)

    def add_messages(self, messages):
        for message in messages:
            self.add_message(*message)

    def get_messages(self):
        return self.messages.values()


class Message:
    def __init__(self, path, line_number):
        self.path = os.path.relpath(path).replace("\\", "/")
        self.line_number = int(line_number)
        self.comments = set()
        self.status = "FOUND"

    def __str__(self):
        return """
Message:
    Path: {0}
    Line number: {1}
    Content: {2}
        """.format(
            self.path, self.line_number, self.comments
        ).strip()

    def append(self, message):
        self.comments.add(message)

    def as_dict(self):
        return {
            "path": self.path,
            "line_number": self.line_number,
            "comments": list(self.comments),
            "status": self.status,
        }
