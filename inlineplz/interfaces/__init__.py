# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.interfaces.github import GitHubInterface

STASH_SUPPORTED = False
try:
    from inlineplz.interfaces.stash import StashInterface
    STASH_SUPPORTED = True
except ImportError:
    pass

INTERFACES = {
    'github': GitHubInterface,
}

if STASH_SUPPORTED:
    INTERFACES['stash'] = StashInterface
