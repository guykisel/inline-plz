# -*- coding: utf-8 -*-

from __future__ import absolute_import

from inlineplz.interfaces.github import GitHubInterface
from inlineplz.interfaces.stash import StashInterface

INTERFACES = {
    'github': GitHubInterface,
    'stash': StashInterface
}
