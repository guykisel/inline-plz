# -*- coding: utf-8 -*-

"""
System utilities
"""


import os
import sys

STOP_FILE_NAME = ".inlineplzstop"

if sys.platform == "win32":
    JAVA_SEP = ";"
else:
    JAVA_SEP = ":"


def should_stop():
    return os.path.isfile(os.path.join(os.getcwd(), STOP_FILE_NAME))


def vendored_path(path):
    # we use a relpath on windows because the colon in windows drive letter paths messes with java classpaths
    if sys.platform == "win32":
        return os.path.normpath(
            os.path.relpath(
                os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", path),
                os.getcwd(),
            )
        )

    return os.path.normpath(
        os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin", path)
        )
    )
