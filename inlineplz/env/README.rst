==========
env
==========

Used in ``inlineplz.main`` to help set arguments / variables based on the current environment. Autodetects running in environments such as Travis or Jenkins to load common environment variables. To add new environments, inherit from EnvBase and add an entry in current_env() in ``__init__.py``.
