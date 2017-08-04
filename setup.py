#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='es_query_builder',
    version='0.1.0',
    description="A Query Builder to build queries specially suited for ElasticSearch queries",
    long_description=readme + '\n\n' + history,
    author="Santiago Saavedra",
    author_email='ssaavedra@openshine.com',
    url='https://github.com/ssaavedra/es_query_builder',
    packages=[
        'es_query_builder',
    ],
    package_dir={'es_query_builder':
                 'es_query_builder'},
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3',
    zip_safe=False,
    keywords='es_query_builder',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
