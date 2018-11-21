# -*- coding: utf-8 -*-

import codecs
import os.path

import inlineplz.linters.clippy as clippy

clippy_path = os.path.join("tests", "testdata", "parsers", "clippy.txt")


def test_clippy():
    with codecs.open(clippy_path, encoding="utf-8", errors="replace") as inputfile:
        messages = sorted(list(clippy.ClippyParser().parse(inputfile.read())))
        assert (
            messages[0][2]
            == 'error: this comparison involving the minimum or maximum element for this type contains a case that is always true or always false\n --> src/main.rs:3:20\n  |\n3 |     println!("{}", x <= 0);\n  |                    ^^^^^^\n  |\n  = note: #[deny(clippy::absurd_extreme_comparisons)] on by default\n  = help: because 0 is the minimum value for this type, the case where the two sides are not equal never occurs, consider using x == 0 instead\n  = help: for further information visit https://rust-lang-nursery.github.io/rust-clippy/v0.0.212/index.html#absurd_extreme_comparisons\n\n'
        )
        assert messages[0][1] == 3
        assert messages[0][0] == "src/main.rs"
