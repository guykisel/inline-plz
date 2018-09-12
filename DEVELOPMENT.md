# Developing inline-plz

`inline-plz` is intended to be compatible with python 3.5 or newer, 3.6 is the recommended version for development.

To get started developing inline-plz, we recommend setting up a `pyenv` `virtualenv` and then running `pip` install the development requirements:

```
$ pyenv virtualenv 3.6.0 inline-plz
$ pip install -r requirements_dev.txt
```

To run `inline-plz` locally

```
$ inline-plz --dryrun --autorun
```

To run the unit tests, use the `tox` runner:

```
$ tox
```

This should run a set of tests against both python 3.5 ad 3.6.


When you submit Pull Requests, `inline-plz` will kick off a [Travis job](https://github.com/guykisel/inline-plz/blob/master/.travis.yml) that ... checks itself!   Please help keep `inline-plz` linted as an shining example of what great looks like!
