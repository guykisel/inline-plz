# Developing inline-plz

`inline-plz` is intended to be compatible with python 3.5 or newer, 3.6 is the recommended version for development.

We recommend following [existing guides](https://docs.python-guide.org/dev/env/) for getting your development environment set up to your liking.

If you're working on Linux or OSX, we recommend setting up a `pyenv` `virtualenv` and then running `pip` install the development requirements:

```bash
$ pyenv virtualenv 3.6.0 inline-plz
$ pip install -r requirements_dev.txt
```

To to a full run of `inline-plz` locally:

```bash
$ inline-plz --dryrun --autorun
```

To run the unit tests, use the `tox` runner:

```bash
$ py.test
$ tox
```

Note: Tox will run the unit tests against python 3.5, 3.6, and 3.7.


When you submit Pull Requests, `inline-plz` will kick off a [Travis job](blob/master/.travis.yml) that ... checks itself!   Please help keep `inline-plz` linted as an shining example of what great looks like!


# Adding New Linters

You've got a new tool for helping improve code bases?  Why let's get 'er supported within `inline-plz`.  Here's where you'll need to look to get your awesome new tool added in with all the others:

`inline-plz` uses external linters, typically installed as their own command line utilities.  To simplify the use of those linters by `inline-plz` users, we request that you implement an installation process in addition to adapting it's output to the format expected by `inline-plz`.

## Configure a File Matcher

If your linter is for a file type not yet supported by `inline-plz`, you'll need to add a pattern matcher in [linters/__init__.py](blob/master/inlineplz/linters/__init__.py) (see `register_patterns`):

```python
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
    # Add your newlang language and file pattern in alphabetic order if you don't mind
    register_pattern("newlang", ["*.newlang"])
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

```


## Create your Linter class and a unit test


Create your linter class in `inlineplz/linters`, then import your linter in [linters/__init__.py](blob/master/inlineplz/linters/__init__.py).

Here is the tflint Linter:

```python
from __future__ import absolute_import
from __future__ import unicode_literals

from inlineplz.decorators import linter
from inlineplz.parsers.base import ParserBase
import dirtyjson as json


@linter(
    {
        "name": "tflint",
        "language": "terraform",
        "patterns": ["*.tf"],
        "install": [["brew", "install", "tflint"]],
        "help": ["tflint", "--help"],
        "run": ["tflint", "--format=json"],
        "rundefault": ["tflint", "--format=json"],
        "dotfiles": [],
        "autorun": True,
        "run_per_file": False,
    }
)
class TFLintParser(ParserBase):
    """Parse tflint output."""


    def parse(self, lint_data):
        messages = set()

        for error_stanza in json.loads(lint_data):
            messages.add(
                (
                    error_stanza.get("file", None),
                    error_stanza.get("line", None),
                    error_stanza.get("message", None),
                )
            )

        return messages
```

There a few things to point out here:

* When the linter being wrapped supports it we recommed having it produce machine readable output.  We find Json to be *very* convienient.
* When processing Json we recommend `dirtyjson` over the standard `json` library.

In the `@linter` annotation, the parameters are:
* `name` should be a unique name for your linter (unique among the other linters, we recommend that this is the same name as your linter's `.py` file).
* `language` this determines the file pattern matchers the linter will be called for, see `register_patterns` above.
* `install` this is a list of lists, each represents the shell commands to be run to perform installation, each will be attempted until one succeeds or all have failed
* `help` how to get help from the tool, this is also used to verify the tool can be called and is installed
* `run` this is the shell command to run your tool with out specifying a configuration file
* `rundefault` this is the shell command to run your tool with the default configuration file embedded in `inline-plz` (see `./inlineplz/linters/config/`)
* `dotfiles` this is a set of default configuration files, embedded in `inline-plz`
* `autorun` this is a boolean variable, when `True` will cause your linter to be run without having to be explicitly called
* `run_per_file` a boolean, if `True`, the linter will be shelled out and called for each file (`run_per_file=True` can be slow), if `False` the linter will be run once for the entire source tree

If your tool is common enough that `inline-plz` should try it out for ever project, consider adding it to `TRUSTED_INSTALL`.

## Optionally Create a Default Configuration

Add a default [configuration](tree/master/inlineplz/linters/config) for the your linter.  This is only necessary if the tool requires a configuration or if you feel the "out of the box" defaults for the new tool should have those defaults overridden.

## Parser Interface

Your parser will need to adapt the output of the linting tool into the structure that `inline-plz` supports.

Parsers must return a python `set()`.  Entries in the set must be a 3-tuple of:

* `string`: file path and name
* `number`: the line number the message refers to
* `string`: message body, the output from the linting tool that refers to this specific file+line number.

```python
  ('project/supercoder.py', 1, "STRONG WARNING: author is a tool")
```

# Integrating with Code Review Tools

See `/guykisel/inline-plz/tree/master/inlineplz/interfaces` for more information.

# Supporting New CI/CD Tooling

See `/guykisel/inline-plz/tree/master/inlineplz/env` for more information.

# Guidelines and Best Practices

Please perform both a `dryrun` and a full `tox` run-through before committing your code.

We'd like to keep the code formatting consistent, and are using the defaults from the [black](https://github.com/ambv/black) python formatting tool as our standard.

