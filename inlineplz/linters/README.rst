==========
linters
==========

Configs for installing and running linters/static analysis tools. ``config`` contains default configs to run these tools with if no local configs are found in the target repo. These configs are intended to be fairly relaxed reasonable defaults that will work well for most repos. To integrate a new tool, add it to ``LINTERS`` in ``__init__.py`` and additionally configure ``PATTERNS`` and ``TRUSTED_INSTALL`` as needed.
