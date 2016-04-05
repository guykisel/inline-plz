===============================
inline-plz
===============================

.. image:: https://img.shields.io/pypi/v/inlineplz.svg
        :target: https://pypi.python.org/pypi/inlineplz

.. image:: https://img.shields.io/travis/guykisel/inline-plz.svg
        :target: https://travis-ci.org/guykisel/inline-plz


Tired of reading through CI console logs to find your lint errors? Inline your lint messages in your diffs!

* Free software: ISC license

Features
--------

* Run linters against your code and comment in your diffs at the failing lines
* Automatically run linters with reasonable default configs
* Easy to add new linter configurations

How to use
----------

::

  pip install inlineplz
  inline-plz --install --autorun


You probably want to run the above in a CI job, not in your regular development environment. 

You'll also need to provide the following either in the command line or via environment variables:

* owner: the repo organization/owner
* repo: the repo name
* token: your auth token (encrypt this, don't put this in plaintext in any public configurations!)
* url: the url of your scm host
* interface: the type of scm host (such as github)

Dependencies:

* node.js / npm
* ruby / gem
* python / pip

Known issues
------------

* Currently for Travis-CI usage, inline-plz only works for PRs within the original repo, not PRs from forks. This is because encrypted creds in Travis-CI configs are encrypted per repo, and cannot be decrypted in PRs from forks.
* Currently the inline-plz console output can print out some misleading stack traces
* Currently dependencies get installed globally unless you pre-create a virtualenv
* Commits directly to master are not currently supported

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
