# -*- coding: utf-8 -*-

import os


class Messages(object):

    def __init__(self):
        self.messages = {}

    def add_message(self, path, line, message):
        if (path, line) not in self.messages:
            self.messages[(path, line)] = Message(path, line)
        self.messages[(path, line)].append(message)


class Message(object):

    def __init__(self, path, line_number):
        self.path = os.path.relpath(path).replace('\\', '/')
        self.line_number = line_number
        self.comments = set()

    def __str__(self):
        return """
Message:
    Path: {0}
    Line number: {1}
    Content: {2}
        """.format(self.path, self.line_number, self.content).strip()

    @property
    def content(self):
        if not self.comments:
            return ''
        if len(self.comments) > 1:
            return '```\n' + '\n'.join(self.comments) + '\n```'
        return '`{0}`'.format(list(self.comments)[0].strip())

    def append(self, message):
        self.comments.add(message)
