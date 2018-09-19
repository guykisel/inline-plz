# -*- coding: utf-8 -*-
# pylint: disable=W0703,C0412
"""Linter configurations."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import sys

from inlineplz.registry import register_pattern

# import your linter here
from inlineplz.linters.ansiblelint import AnsibleLintParser  # NOQA
from inlineplz.linters.bandit import BanditParser  # NOQA
from inlineplz.linters.codenarc import CodenarcParser  # NOQA
from inlineplz.linters.coala import CoalaParser  # NOQA
from inlineplz.linters.detectsecrets import DetectSecretsParser  # NOQA
from inlineplz.linters.dockerfilelint import DockerfileLintParser  # NOQA
from inlineplz.linters.eclint import ECLintParser  # NOQA
from inlineplz.linters.eslint import ESLintParser  # NOQA
from inlineplz.linters.gherkinlint import GherkinLintParser  # NOQA
from inlineplz.linters.gometalinter import GometalinterParser  # NOQA
from inlineplz.linters.htmlhint import HTMLHintParser  # NOQA
from inlineplz.linters.jscs import JSCSParser  # NOQA
from inlineplz.linters.jshint import JSHintParser  # NOQA
from inlineplz.linters.jsonlint import JSONLintParser  # NOQA
from inlineplz.linters.markdownlint import MarkdownLintParser  # NOQA
from inlineplz.linters.megacheck import MegacheckParser  # NOQA
from inlineplz.linters.pmd import PMDParser  # NOQA
from inlineplz.linters.proselint import ProselintParser  # NOQA
from inlineplz.linters.prospector import ProspectorParser  # NOQA
from inlineplz.linters.rflint import RobotFrameworkLintParser  # NOQA
from inlineplz.linters.rstlint import RSTLintParser  # NOQA
from inlineplz.linters.shellcheck import ShellcheckParser  # NOQA
from inlineplz.linters.spotbugsmaven import SpotbugsMavenParser  # NOQA
from inlineplz.linters.stylint import StylintParser  # NOQA
from inlineplz.linters.tflint import TFLintParser  # NOQA
from inlineplz.linters.yamllint import YAMLLintParser  # NOQA


def register_patterns():
    register_pattern("all", ["*.*"])
    register_pattern("ansible", ["*.yaml", "*.yml"])
    register_pattern("docker", ["*Dockerfile", "*.dockerfile"])
    register_pattern("gherkin", ["*.feature"])
    register_pattern("go", ["*.go"])
    register_pattern("groovy", ["*.groovy", "Jenkinsfile", "jenkinsfile"])
    register_pattern("java", ["*.java"])
    register_pattern("javascript", ["*.js"])
    register_pattern("json", ["*.json"])
    register_pattern("html", ["*.html", "*.htm"])
    register_pattern("markdown", ["*.md"])
    register_pattern("python", ["*.py"])
    register_pattern("shell", ["*.sh", "*.zsh", "*.ksh", "*.bsh", "*.csh", "*.bash"])
    register_pattern("stylus", ["*.styl"])
    register_pattern("robotframework", ["*.robot"])
    register_pattern("rst", ["*.rst"])
    register_pattern(
        "text", ["*.md", "*.txt", "*.rtf", "*.html", "*.tex", "*.markdown"]
    )
    register_pattern("yaml", ["*.yaml", "*.yml"])


def init():
    register_patterns()


# TODO: can we not do this at "compile" or "import" time?
init()


# these commands will be autorun to try to install dependencies.
TRUSTED_INSTALL = [
    ["bundle", "install"],
    ["cabal", "update"],
    ["cabal", "install"],
    ["glide", "install", "--strip-vendor"],
    ["godep", "get"],
    ["godep", "restore"],
    ["dep", "ensure"],
    ["dep", "prune"],
    ["govendor", "sync"],
    ["go", "get", "-t", "-v", "./..."],
    ["yarn", "install", "--non-interactive"],
    ["npm", "install"],
    [sys.executable, "setup.py", "develop"],
    [sys.executable, "-m", "pip", "install", "."],
    [sys.executable, "-m", "pip", "install", "-e", "."],
    [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
    [sys.executable, "-m", "pip", "install", "-r", "requirements_dev.txt"],
    [sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"],
    ["pipenv", "install"],
]

# these dirs will get deleted after a run
INSTALL_DIRS = ["node_modules", ".bundle"]
