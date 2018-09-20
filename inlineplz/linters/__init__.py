# -*- coding: utf-8 -*-
# pylint: disable=W0703,C0412
"""Linter configurations."""


import sys

from ..registry import register_pattern

# import your linter here
from ..linters.ansiblelint import AnsibleLintParser  # NOQA
from ..linters.bandit import BanditParser  # NOQA
from ..linters.codenarc import CodenarcParser  # NOQA
from ..linters.coala import CoalaParser  # NOQA
from ..linters.detectsecrets import DetectSecretsParser  # NOQA
from ..linters.dockerfilelint import DockerfileLintParser  # NOQA
from ..linters.eclint import ECLintParser  # NOQA
from ..linters.eslint import ESLintParser  # NOQA
from ..linters.gherkinlint import GherkinLintParser  # NOQA
from ..linters.gometalinter import GometalinterParser  # NOQA
from ..linters.htmlhint import HTMLHintParser  # NOQA
from ..linters.jscs import JSCSParser  # NOQA
from ..linters.jshint import JSHintParser  # NOQA
from ..linters.jsonlint import JSONLintParser  # NOQA
from ..linters.markdownlint import MarkdownLintParser  # NOQA
from ..linters.megacheck import MegacheckParser  # NOQA
from ..linters.pmd import PMDParser  # NOQA
from ..linters.proselint import ProselintParser  # NOQA
from ..linters.prospector import ProspectorParser  # NOQA
from ..linters.rflint import RobotFrameworkLintParser  # NOQA
from ..linters.rstlint import RSTLintParser  # NOQA
from ..linters.shellcheck import ShellcheckParser  # NOQA
from ..linters.spotbugsmaven import SpotbugsMavenParser  # NOQA
from ..linters.stylint import StylintParser  # NOQA
from ..linters.tflint import TFLintParser  # NOQA
from ..linters.yamllint import YAMLLintParser  # NOQA


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
