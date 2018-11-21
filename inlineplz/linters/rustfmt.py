# -*- coding: utf-8 -*-


from ..decorators import linter
from ..parsers.base import ParserBase


@linter(
    name="rustfmt",
    install=["rustup", "component", "add", "rustfmt-preview"],
    help_cmd=["rustfmt", "--help"],
    run=["cargo", "fmt", "--quiet", "--all"],
    rundefault=[
        "cargo",
        "fmt",
        "--quiet",
        "--all",
        "--",
        "--config-path={config_dir}/.rustfmt.toml",
    ],
    dotfiles=[".rustfmt.toml"],
    language="rust",
    autorun=False,
    run_per_file=False,
    autofix=True,
)
class RustfmtParser(ParserBase):
    """rustfmt isn't actually a linter, so no-op."""

    def parse(self, lint_data):
        return []
