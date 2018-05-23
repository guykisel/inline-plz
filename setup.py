#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'unidiff',
    'github3.py',
    'xmltodict',
    'pyyaml',
    'scandir',
    'uritemplate.py',
    'dirtyjson',
    'python-dateutil',
    'git-url-parse'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='inlineplz',
    version='0.35.0',
    description="Inline your lint messages",
    long_description=readme + '\n\n' + history,
    author="Guy Kisel",
    author_email='guy.kisel@gmail.com',
    url='https://github.com/guykisel/inline-plz',
    packages=find_packages('.', exclude=('tests*', 'testing*')),
    include_package_data=True,
    install_requires=requirements,
    license="ISCL",
    zip_safe=False,
    keywords='inlineplz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    entry_points={
        'console_scripts': [
            'inline-plz = inlineplz.main:main'
        ],
    }
)
