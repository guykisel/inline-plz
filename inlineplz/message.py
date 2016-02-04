# -*- coding: utf-8 -*-

import os
import traceback


class Messages(object):

    def __init__(self):
        self.messages = {}

    def add_message(self, path, line, message):
        if (path, line) not in self.messages:
            try:
                self.messages[(path, line)] = Message(path, line)
            except TypeError:
                traceback.print_exc()
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
        """.format(self.path, self.line_number, self.content).strip()

    def append(self, message):
        self.comments.add(message)
