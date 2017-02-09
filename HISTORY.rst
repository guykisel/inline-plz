=======
History
=======

0.19.0 (2016-07-17)
-------------------

* Add out of date check
* Config improvements

0.18.0 (2016-06-19)
-------------------

* Add gometalinter support
* Catch index errors in some parsers

0.17.0 (2016-06-12)
-------------------

* Add --trusted flag for installs
* Cleanup install dirs before run

0.16.1 (2016-06-08)
-------------------

* Fix path to markdownlint

0.16.0 (2016-06-05)
-------------------

* Run 'bundle install' during ruby gem installs
* Replace ruby markdownlint with node.js markdownlint
* Enable or disable linters in yaml

0.15.0 (2016-05-21)
-------------------

* Add bandit support

0.14.0 (2016-05-21)
-------------------

* Stringify error output
* Use time.time instead of time.clock
* Check github url
* Add dockerfile_lint support
* Add shellcheck support
* Run prospector with optional extras

0.13.0 (2016-04-19)
-------------------

* Add support for gherkin-lint
* Configure rflint to run per file
* Set jscs autorun to False
* Update eslint dotfiles

0.12.5 (2016-04-14)
-------------------

* Minor improvements to logging
* Add explicit jscs dir exclusions

0.12.4 (2016-04-13)
-------------------

* Encode output to ascii and replace errors

0.12.3 (2016-04-13)
-------------------

* Don't use unicode literals in setup.py

0.12.2 (2016-04-13)
-------------------

* Use unicode literals instead of decoding utf-8
* Set npm progress=false

0.12.1 (2016-04-12)
-------------------

* Replace decode errors

0.12.0 (2016-04-12)
-------------------

* Log all install output
* Set max comments per file in github interface

0.11.0 (2016-03-29)
-------------------

* Tell utf-8 encoder to replace errors
* Robotframework lint support

0.10.1 (2016-03-16)
-------------------

* Fix .mdlrc syntax

0.10.0 (2016-03-15)
-------------------

* Improve performance

0.9.0 (2016-03-14)
------------------

* Print installation and lint durations

0.8.2 (2016-03-11)
------------------

* Remove bad whitespace from stylint dotfile name

0.8.1 (2016-03-11)
------------------

* Detect yaml-lint install using just yaml-lint

0.8.0 (2016-02-29)
------------------

* Add --config-dir arg
* Add stylint support
* Add default mdl config

0.7.5 (2016-02-22)
------------------

* Quit early if no interface found

0.7.4 (2016-02-18)
------------------

* Catch OSError during install

0.7.3 (2016-02-18)
------------------

* Don't re-run install commands
* Better error handling

0.7.2 (2016-02-17)
------------------

* Handle missing config file

0.7.1 (2016-02-17)
------------------

* Load paths to ignore from yaml config

0.7.0 (2016-02-16)
------------------

* Add jsonlint support
* Add yaml-lint support
* Fix running per file
* Add restructuredtest-lint support
* Add markdownlint support

0.6.0 (2016-02-12)
------------------

* Only autorun if no dotfiles found for language

0.5.5 (2016-02-12)
------------------

* Catch GitHubError

0.5.4 (2016-02-12)
------------------

* Use os.walk instead of glob for file search
* Normalize message paths before storing

0.5.3 (2016-02-12)
------------------

* Include linter config files in MANIFEST.in

0.5.2 (2016-02-12)
------------------

* Fix installed check

0.5.1 (2016-02-12)
------------------

* Update deploy config
* Better installation

0.5.0 (2016-02-11)
------------------

* Unpin dependencies
* Add autorun mode
* Do a release on travis python version == 2.7

0.4.1 (2016-02-10)
------------------

* Load owner and repo from ghprbPullLink

0.4.0 (2016-02-08)
------------------

* Catch Exception on run
* Prepend linter name to message content

0.3.2 (2016-02-05)
------------------

* For js linters, just 'npm install'

0.3.1 (2016-02-05)
------------------

* Fix for jshint xml parsing

0.3.0 (2016-02-04)
------------------

* Add --max-comments arg

0.2.0 (2016-02-04)
------------------

* Disable running if not in a PR or if no Github is defined

0.1.1 (2016-02-03)
------------------

* Initial release supporting prospector, jshint, eslint, jscs

0.1.0 (2015-12-13)
------------------

* First release on PyPI.
