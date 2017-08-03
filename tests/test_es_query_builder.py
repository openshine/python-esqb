#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_es_query_builder
----------------------------------

Tests for `es_query_builder` module.
"""

import pytest


from es_query_builder import es_query_builder


@pytest.fixture
def response():
    """Sample pytest fixture.
    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument.
    """
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
