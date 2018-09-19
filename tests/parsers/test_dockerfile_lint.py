# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.dockerfilelint as dockerfilelint

dockerfilelint_path = os.path.join(
    "tests", "testdata", "parsers", "dockerfile_lint.txt"
)


def test_dockerfilelint():
    with codecs.open(
        dockerfilelint_path, encoding="utf-8", errors="replace"
    ) as inputfile:
        messages = sorted(
            list(
                dockerfilelint.DockerfileLintParser().parse(
                    [("fakefile.txt", inputfile.read())]
                )
            )
        )
        assert messages[0][2] == "Required LABEL name/key 'Name' is not defined"
        assert messages[0][1] == -1
        assert messages[0][0] == "fakefile.txt"
