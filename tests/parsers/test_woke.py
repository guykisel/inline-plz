# -*- coding: utf-8 -*-

import codecs
import os

import inlineplz.linters.woke as woke

woke_path = os.path.join("tests", "testdata", "parsers", "woke.txt")

expected_messages = list()
expected_messages.append(
    ("sql/core/src/main/scala/org/apache/spark/sql/execution/joins/HashedRelation.scala", 406, "`dummy` may be insensitive, use `placeholder`, `sample` instead (error)")
)
expected_messages.append(
    ("sql/core/src/main/scala/org/apache/spark/sql/execution/datasources/FileFormatWriter.scala", 208, "`dummy` may be insensitive, use `placeholder`, `sample` instead (error)")
)
expected_messages.append(
    ("docs/js/vendor/bootstrap.bundle.min.js.map", 1, "`whiteList` may be insensitive, use `allowlist`, `inclusion list` instead (warning)")
)
expected_messages.append(
    ("sql/core/src/main/scala/org/apache/spark/sql/execution/adaptive/InsertAdaptiveSparkPlan.scala", 107, "`sanity` may be insensitive, use `confidence`, `quick check`, `coherence check` instead (error)")
)
expected_messages = sorted(expected_messages)


def test_woke():
    with codecs.open(woke_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(woke.WokeParser().parse(inputfile.read())))
        assert len(expected_messages) == len(messages)

        for i in range(len(messages)):
            assert messages[i][2] == expected_messages[i][2]
            assert messages[i][1] == expected_messages[i][1]
            assert messages[i][0] == expected_messages[i][0]
