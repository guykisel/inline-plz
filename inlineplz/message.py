# -*- coding: utf-8 -*-


class Message(object):

    def __init__(self, path, line_number):
        self.path = path.replace('\\', '/')
        self.line_number = line_number
        self.comments = []

    def __str__(self):
        return """
Message:
    Path: {0}
    Line number: {1}
    Content: {2}
        """.format(self.path, self.line_number, self.content).strip()

    @property
    def content(self):
        return '```\n' + '\n'.join(self.comments) + '\n```'
