# -*- coding: utf-8 -*-

import requests
import random

from inlineplz.interfaces.base import InterfaceBase

class SwarmInterface(InterfaceBase):
    def __init__(self, username, password, host, topic, version='v8'):
        self.username = username
        self.password = password
        self.host = host
        self.topic = topic
        self.version = version

    def post_messages(self, messages, max_comments):
        # randomize message order to more evenly distribute messages across different files
        messages = list(messages)
        random.shuffle(messages)

        messages_to_post = 0
        messages_posted = 0
        current_comments = self.get_comments(max_comments)
        for msg in messages:
            if not msg.comments:
                continue
            messages_to_post += 1
            body = self.format_message(msg)
            if self.is_duplicate(current_comments, msg, body):
                continue
            # try to send swarm post comment
            self.post_comment(msg)
            messages_posted += 1
            if max_comments >= 0 and messages_posted > max_comments:
                break
        print('{} messages posted to Swarm.'.format(messages_to_post))
        return messages_to_post

    def post_comment(self, msg):
        # https://www.perforce.com/perforce/doc.current/manuals/swarm/index.html#Swarm/swarm-apidoc.html#Comments___Swarm_Comments%3FTocPath%3DSwarm%2520API%7CAPI%2520Endpoints%7C_____3
        url = "https://{}/api/{}/comments".format(self.host, self.version)
        payload = {
            'topic': self.topic,
            'body': self.format_message(msg),
            'context[file]': msg.path,
            'context[rightLine]': msg.line_number
        }
        r = requests.post(url, auth=(self.username, self.password), data=payload)

    def get_comments(self, max_comments=100):
        # https://www.perforce.com/perforce/doc.current/manuals/swarm/index.html#Swarm/swarm-apidoc.html#Comments___Swarm_Comments%3FTocPath%3DSwarm%2520API%7CAPI%2520Endpoints%7C_____3
        parameters = "topic={}&max={}".format(self.topic, max_comments)
        url = "https://{}/api/{}/comments".format(self.host, self.version)
        r = requests.get(url, auth=(self.username, self.password))
        if (r.status_code != 200):
            return {}
        return r.json()["comments"]

    @staticmethod
    def is_duplicate(comments, msg, body):
        for comment in comments:
            try:
                if (comment["context"]["rightLine"] == msg.line_number):
                    if (comment["context"]["file"] == msg.path):
                        if (comment["body"].strip() == body.strip()):
                            return True
            except (KeyError, TypeError) as e:
                continue
        return False

    @staticmethod
    def format_message(message):
        if not message.comments:
            return ''
        if len(message.comments) > 1:
            return (
                '```\n' +
                '\n'.join(sorted(list(message.comments))) +
                '\n```'
            )
        return '`{0}`'.format(list(message.comments)[0].strip())

