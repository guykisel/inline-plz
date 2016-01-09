# -*- coding: utf-8 -*-


class Message(object):

    def __init__(self, path, line_number, content):
        self.path = path
        self.line_number = line_number
        self.content = content
