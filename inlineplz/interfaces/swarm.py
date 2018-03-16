# -*- coding: utf-8 -*-

import random
import subprocess

import requests

from inlineplz.interfaces.base import InterfaceBase

class SwarmInterface(InterfaceBase):
    def __init__(self, args):
        """
        SwarmInterface lets us post messages to Swarm (Helix).

        username and password are the credentials used to access Swarm/Perforce.
        host is the server (And any additional paths before the api)
        topic is the the review you are commenting on (for reviews, it will typically be "review/###" for some review number)
        """
        review_id = args.review_id
        try:
            review_id = int(review_id)
        except (ValueError, TypeError):
            print('{0} is not a valid review ID'.format(review_id))
            return
        self.username = args.username
        self.password = args.password
        self.host = args.host
        self.topic = "review/{}".format(review_id)
        # current implementation uses version 8 of the implementation
        # https://www.perforce.com/perforce/doc.current/manuals/swarm/index.html#Swarm/swarm-apidoc.html#Swarm_API%3FTocPath%3DSwarm%2520API%7C_____0
        self.version = 'v8'

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
            proc = subprocess.Popen(["p4", "fstat", "-T", "depotFile", msg.path], stdout=subprocess.PIPE)
            output = proc.stdout.read()
            l = output.split()
            if (len(l) != 3):
                print("Can't find depotFile for '{}': {}".format(msg.path, output))
                continue
            path = output.split()[2]
            if self.is_duplicate(current_comments, body, path, msg.line_number):
                print("Duplicate for {}:{}".format(path, msg.line_number))
                continue
            # try to send swarm post comment
            self.post_comment(body, path, msg.line_number)
            messages_posted += 1
            if max_comments >= 0 and messages_posted > max_comments:
                break
        print('{} messages posted to Swarm.'.format(messages_to_post))
        return messages_to_post

    def post_comment(self, body, path, line_number):
        # https://www.perforce.com/perforce/doc.current/manuals/swarm/index.html#Swarm/swarm-apidoc.html#Comments___Swarm_Comments%3FTocPath%3DSwarm%2520API%7CAPI%2520Endpoints%7C_____3
        url = "https://{}/api/{}/comments".format(self.host, self.version)
        payload = {
            'topic': self.topic,
            'body': body,
            'context[file]': path,
            'context[rightLine]': line_number
        }
        print("".format(payload))
        requests.post(url, auth=(self.username, self.password), data=payload)

    def get_comments(self, max_comments=100):
        # https://www.perforce.com/perforce/doc.current/manuals/swarm/index.html#Swarm/swarm-apidoc.html#Comments___Swarm_Comments%3FTocPath%3DSwarm%2520API%7CAPI%2520Endpoints%7C_____3
        parameters = "topic={}&max={}".format(self.topic, max_comments)
        url = "https://{}/api/{}/comments?{}".format(self.host, self.version, parameters)
        response = requests.get(url, auth=(self.username, self.password))
        if (response.status_code != requests.codes.ok):
            print("Can't get comments, status code: {}".format(response.status_code))
            return {}
        return response.json()["comments"]

    @staticmethod
    def is_duplicate(comments, body, path, line_number):
        for comment in comments:
            try:
                if (comment["context"]["rightLine"] == line_number and
                    comment["context"]["file"] == path and
                    comment["body"].strip() == body.strip()):
                    print("Dupe: {}:{}".format(comment["context"]["file"], comment["context"]["rightLine"]))
                    return True
            except (KeyError, TypeError):
                continue
        return False

    @staticmethod
    def format_message(message):
        if not message.comments:
            return ''
        return (
            '```\n' +
            '\n'.join(sorted(list(message.comments))) +
            '\n```'
        )
