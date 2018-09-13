# Developing inline-plz

`inline-plz` is intended to be compatible with python 3.5 or newer, 3.6 is the recommended version for development.

We recommend following [existing guides](https://docs.python-guide.org/dev/env/) for getting your development environment set up to your liking.

If you're working on Linux or OSX, we recommend setting up a `pyenv` `virtualenv` and then running `pip` install the development requirements:

```bash
$ pyenv virtualenv 3.6.0 inline-plz
$ pip install -r requirements_dev.txt
```

To run `inline-plz` locally

```bash
$ inline-plz --dryrun --autorun
```

To run the unit tests, use the `tox` runner:

```bash
$ tox
```

This should run a set of tests against both python 3.5 add 3.6.


When you submit Pull Requests, `inline-plz` will kick off a [Travis job](blob/master/.travis.yml) that ... checks itself!   Please help keep `inline-plz` linted as an shining example of what great looks like!


# Adding New Linters

You've got a new tool for helping improve code bases?  Why let's get 'er supported within `inline-plz`.  Here's where you'll need to look to get your awesome new tool added in with all the others:

`inline-plz` uses external linters, typically installed as their own command line utilities.  To simplify the use of those linters by `inline-plz` users, we request that you implement an installation process

## Configure a File Matcher

Set up file pattern matchers in [linters/__init__.py](blob/master/inlineplz/linters/__init__.py) (see `PATTERNS`).

```python
PATTERNS = {
    ...
    "ansible": ["*.yaml", "*.yml"],
    ...
}
```


## Configure Auto Installation and Create an Execution Configuration

Add configuration for executing your linter [linters/__init__.py](blob/master/inlineplz/linters/__init__.py) (see `LINTERS`).

```python
LINTERS = {
    "ansible-lint": {
        "install": [[sys.executable, "-m", "pip", "install", "-U", "ansible-lint"]],
        "help": ["ansible-lint", "-h"],
        "run": ["ansible-lint", "-p"],
        "rundefault": ["ansible-lint", "-p", "-c", "{config_dir}/.ansible-lint"],
        "dotfiles": [".ansible-lint"],
        "parser": parsers.AnsibleLintParser,
        "language": "ansible",
        "autorun": True,
        "run_per_file": True,
    },
    ...
}
```

We'd appreciate it if you kept these in alphabetical order,

If your tool is common enough that `inline-plz` should try it out for ever project, consider adding it to `TRUSTED_INSTALL`.

## Optionally Create a Default Configuration

Add a default [configuration](tree/master/inlineplz/linters/config) for the your linter.  This is only necessary if the tool requires a configuration or if you feel the "out of the box" defaults for the new tool should have those defaults overridden.

## Implement your Parser

Implement a [parser](tree/master/inlineplz/parsers) to adapt the output of the linting tool into the structure that `inline-plz` supports.

Please name your parser's `.py` file with the name of your linting tool.  Note that the class name here must match the class referred to in the `LINTERS` map above, eg: `parsers.AnsibleLintParser`.

Parsers must return a python `set()`.  Entries in the set must be a 3-tuple of:

* string: file path and name
* number: the line number the message refers to
* string: message body, the output from the linting tool that refers to this specific file+line number.

```python
  ('project/supercoder.py', 1, "STRONG WARNING: author is a tool")
```


```python
class AnsibleLintParser(ParserBase):
    """Parse Ansible Lint output."""

    def parse(self, lint_data):
        messages = set()
        for file_path, output in lint_data:
            if file_path.strip() and output.strip():
                for line in output.split("\n"):
                    try:
                        if line.strip():
                            parts = line.split(":")
                            path = parts[0].strip()
                            line_no = int(parts[1].strip())
                            msgbody = parts[2].strip()
                            messages.add((path, line_no, msgbody))
                    except (ValueError, IndexError, TypeError):
                        print("Invalid message: {0}".format(line))
        return messages

```

Import your parser in `inlineplz/parser/__init__.py`.

# Integrating with Code Review Tools

See `/guykisel/inline-plz/tree/master/inlineplz/interfaces` for more information.

# Supporting New CI/CD Tooling

See `/guykisel/inline-plz/tree/master/inlineplz/env` for more information.

# Guidelines and Best Practices

Please perform both a `dryrun` and a full `tox` run-through before committing your code.

We'd like to keep the code formatting consistent, and are using the defaults from the [black](https://github.com/ambv/black) python formatting tool as our standard.

