#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import pprint
import sys
import time
import traceback

import giturlparse
import yaml

from . import __version__, env, interfaces
from .linter_runner import LinterRunner


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pull-request", type=int)
    parser.add_argument("--owner", type=str)
    parser.add_argument("--repo", type=str)
    parser.add_argument("--repo-slug", type=str)
    parser.add_argument("--branch", type=str)
    parser.add_argument("--token", type=str)
    parser.add_argument("--commit", type=str, help="commit hash or number")
    parser.add_argument("--interface", type=str, choices=interfaces.INTERFACES)
    parser.add_argument("--url", type=str)
    parser.add_argument("--enabled-linters", type=str, nargs="+")
    parser.add_argument("--disabled-linters", type=str, nargs="+")
    parser.add_argument("--dryrun", action="store_true")
    parser.add_argument("--zero-exit", action="store_true")
    parser.add_argument("--install", action="store_true")
    parser.add_argument("--prefix", type=str, default="[inline-plz]")
    parser.add_argument("--delete-outdated", action="store_true")
    parser.add_argument(
        "--trusted", action="store_true", help="allow installing all local dependencies"
    )
    parser.add_argument(
        "--max-comments", default=25, type=int, help="maximum comments to write"
    )
    parser.add_argument(
        "--autorun",
        action="store_true",
        help="automatically run linters with reasonable defaults",
    )
    parser.add_argument(
        "--config-dir", help="default directory to search for linter config files"
    )
    args = parser.parse_args()
    args = env.update_args(args)
    if args.config_dir:
        args.config_dir = os.path.abspath(args.config_dir)
        if not os.path.exists(args.config_dir):
            args.config_dir = None
    print("inline-plz version: {}".format(__version__))
    print("Python version: {}".format(sys.version))
    start = time.time()
    result = inline(args)
    print("inline-plz version: {}".format(__version__))
    print("Python version: {}".format(sys.version))
    # TODO: This time is shorter than the longest running linter task in Travis CI somehow??
    print("inline-plz ran for {} seconds".format(int(time.time() - start)))
    print("inline-plz returned exit code {}".format(result))
    return result


def update_from_config(args, config):
    blacklist = [
        "trusted",
        "token",
        "interface",
        "owner",
        "repo",
        "config_dir" "repo_slug",
        "pull_request",
        "zero_exit",
        "dryrun",
        "url",
        "branch",
    ]
    for key, value in config.items():
        if not key.startswith("_") and key not in blacklist:
            if args.__dict__.get(key) and value:
                try:
                    args.__dict__[key].extend(value)
                    args.__dict__[key] = list(set(args.__dict__[key]))
                    continue

                except Exception:
                    traceback.print_exc()
            args.__dict__[key] = args.__dict__.get(key) or value
    return args


def load_config(args, config_path=".inlineplz.yml"):
    """Load inline-plz config from yaml config file with reasonable defaults."""
    config = {}
    print(config_path)
    try:
        with open(config_path) as configfile:
            config = yaml.safe_load(configfile) or {}
            if config:
                print("Loaded config from {}".format(config_path))
                pprint.pprint(config)
    except (IOError, OSError, yaml.parser.ParserError):
        traceback.print_exc()
    args = update_from_config(args, config)
    args.ignore_paths = args.__dict__.get("ignore_paths") or [
        "node_modules",
        ".git",
        ".tox",
        "godeps",
        "vendor",
        "site-packages",
    ]
    if config_path != ".inlineplz.yml":
        return args

    # fall back to config_dir inlineplz yaml if we didn't find one locally
    if args.config_dir and not config:
        new_config_path = os.path.join(args.config_dir, config_path)
        if os.path.exists(new_config_path):
            return load_config(args, new_config_path)

    return args


def inline(args):
    """
    Parse input file with the specified parser and post messages based on lint output

    :param args: Contains the following
        interface: How are we going to post comments?
        owner: Username of repo owner
        repo: Repository name
        pr: Pull request ID
        token: Authentication for repository
        url: Root URL of repository (not your project) Default: https://github.com
        dryrun: Prints instead of posting comments.
        zero_exit: If true: always return a 0 exit code.
        install: If true: install linters.
        max_comments: Maximum comments to write
    :return: Exit code. 1 if there are any comments, 0 if there are none.
    """
    # don't load trusted value from config because we don't trust the config
    trusted = args.trusted
    args = load_config(args)
    print("Args:")
    pprint.pprint(args)
    ret_code = 0

    # TODO: consider moving this git parsing stuff into the github interface
    url = args.url
    if args.repo_slug:
        owner = args.repo_slug.split("/")[0]
        repo = args.repo_slug.split("/")[1]
    else:
        owner = args.owner
        repo = args.repo
    if args.url:
        try:
            url_to_parse = args.url
            # giturlparse won't parse URLs that don't end in .git
            if not url_to_parse.endswith(".git"):
                url_to_parse += ".git"
            parsed = giturlparse.parse(str(url_to_parse))
            url = parsed.resource
            if not url.startswith("https://"):
                url = "https://" + url
            if parsed.owner:
                owner = parsed.owner
            if parsed.name:
                repo = parsed.name
        except giturlparse.parser.ParserError:
            pass
    if not args.dryrun and args.interface not in interfaces.INTERFACES:
        print("Valid inline-plz config not found")
        return 1

    print("Using interface: {0}".format(args.interface))
    my_interface = None
    if not args.dryrun:
        my_interface = interfaces.INTERFACES[args.interface](
            owner,
            repo,
            args.pull_request,
            args.branch,
            args.token,
            url,
            args.commit,
            args.ignore_paths,
            args.prefix,
        )
        if not my_interface.is_valid():
            print("Invalid review. Exiting.")
            return 0

        my_interface.start_review()
    try:
        linter_runner = LinterRunner(
            args.install,
            args.autorun,
            args.ignore_paths,
            args.config_dir,
            args.enabled_linters,
            args.disabled_linters,
            trusted,
        )
        messages = linter_runner.run_linters()
    except Exception:  # pylint: disable=broad-except
        print("Linting failed:\n{}".format(traceback.format_exc()))
        print("inline-plz version: {}".format(__version__))
        print("Python version: {}".format(sys.version))
        ret_code = 1
        if my_interface:
            my_interface.finish_review(error=True)
        return ret_code

    print("{} lint messages found".format(len(messages)))
    print("inline-plz version: {}".format(__version__))
    print("Python version: {}".format(sys.version))

    # TODO: implement dryrun as an interface instead of a special case here

    if args.dryrun:
        print_messages(messages)
        write_messages_to_json(messages)
        return ret_code

    try:
        if my_interface.post_messages(messages, args.max_comments):
            if not args.zero_exit:
                ret_code = 1
            if args.delete_outdated:
                my_interface.clear_outdated_messages()
            my_interface.finish_review(success=False)
            return ret_code

        if args.delete_outdated:
            my_interface.clear_outdated_messages()
        my_interface.finish_review(success=True)
    except KeyError:
        print("Interface not found: {}".format(args.interface))
        traceback.print_exc()
    write_messages_to_json(messages)
    return ret_code


def print_messages(messages):
    for msg in sorted([str(msg) for msg in messages]):
        print(msg)
    print("{} lint messages found".format(len(messages)))


def write_messages_to_json(messages, filename="messages.json"):
    with open(filename, "w") as outfile:
        json.dump([msg.as_dict() for msg in messages], outfile)


if __name__ == "__main__":
    exit(main())
