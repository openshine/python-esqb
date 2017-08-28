#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_esqb
----------------------------------

Tests for `esqb` module.
"""

from esqb import queryfilter, query, variable

testvar = variable.Variable('t')


def test_queryfilter_adds_optional_vars_if_filter_optional_and_vars_required():
    class QF(queryfilter.QueryFilter):
        required = False
        variables = {
            't': variable.Variable('t', required=True)
        }

        def apply(self, query):
            return query

    class Q(query.BaseQuery):
        filters = [QF()]

    assert len(Q().find_all_variables()) == 1
    assert Q().find_all_variables()[0].required is False


def test_queryfilter_adds_required_vars_if_filter_required_and_vars_required():
    class QF(queryfilter.QueryFilter):
        required = True
        variables = {
            't': variable.Variable('t', required=True)
        }

        def apply(self, query):
            return query

    class Q(query.BaseQuery):
        filters = [QF()]

    assert len(Q().find_all_variables()) == 1
    assert Q().find_all_variables()[0].required is True


def test_queryfilter_adds_optional_vars_if_filter_required_and_vars_optional():
    class QF(queryfilter.QueryFilter):
        variables = {
            't': variable.Variable('t', required=True)
        }

        def apply(self, query):
            return query

    class Q(query.BaseQuery):
        filters = [QF()]

    assert len(Q().find_all_variables()) == 1
    assert Q().find_all_variables()[0].required is False


def test_queryfilter_filters_query():
    class QF(queryfilter.QueryFilter):
        variables = {
            't': variable.Variable('t', required=True)
        }

        def apply(self, query, data):
            return {"a": "b"}

    class Q(query.BaseQuery):
        filters = [QF()]

    assert Q().get_es_query({}) == {
        'aggs': {},
        'query': {},
        'size': 0,
        'sort': []
    }
    assert Q().get_es_query({'t': 'x'}) == \
        {'aggs': {},
         'query': {'a': 'b'},
         'size': 0,
         'sort': []
         }
