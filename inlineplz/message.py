# -*- coding: utf-8 -*-

"""Wrap linter messages in a generic Message class that can do some internal cleanup."""

from __future__ import print_function
from __future__ import unicode_literals

import os
import traceback


class Messages(object):

    def __init__(self):
        self.messages = {}

    def add_message(self, path, line, message):
        path = os.path.relpath(path).replace('\\', '/').strip()
        # replace backticks with single quotes to avoid markdown escaping issues
        message = message.replace('`', '\'').strip()
        try:
            line = int(line)
        except (ValueError, TypeError):
            line = 0
        if (path, line) not in self.messages:
            try:
                self.messages[(path, line)] = Message(path, line)
            except TypeError:
                print('{0} {1} {2}'.format(path, line, message))
                traceback.print_exc()
                return
        self.messages[(path, line)].append(message)

    def add_messages(self, messages):
        for message in messages:
            self.add_message(*message)

    def get_messages(self):
        return self.messages.values()


class Message(object):

    def __init__(self, path, line_number):
        self.path = os.path.relpath(path).replace('\\', '/')
        self.line_number = int(line_number)
        self.comments = set()

    def __str__(self):
        return """
Message:
    Path: {0}
    Line number: {1}
    Content: {2}
        """.format(self.path, self.line_number, self.comments).strip()

    def append(self, message):
        self.comments.add(message)
