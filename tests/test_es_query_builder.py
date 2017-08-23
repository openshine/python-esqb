#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_esqb
----------------------------------

Tests for `esqb` module.
"""

from esqb import query, variable

testvar = variable.Variable('t')


class Query(query.BaseQuery):
    aggs = {
        'x': testvar
    }


def test_contains_var():
    assert testvar in Query().find_all_variables()


def test_can_override_var():
    q = Query().get_es_query({'t': 'v'})
    assert q['aggs'] == {'x': 'v'}
    assert q['query'] == {}
    assert q['size'] == 0


def test_uses_default_value():
    class RQuery(query.BaseQuery):
        aggs = {
            'x': variable.Variable(
                't', type=bool,
                required=False,
                default=True)
        }

    q = RQuery()
    assert q.get_es_query({})['aggs'] == {'x': True}


def test_throws_on_missing_required():
    class RQuery(query.BaseQuery):
        aggs = {
            'x': variable.Variable(
                't', type=bool,
                required=True
            )
        }

    q = RQuery()
    try:
        assert q.get_es_query({})
    except Exception:
        pass


def test_complex_query_contains_multiple_vars():
    class RQuery(query.BaseQuery):
        aggs = {
            'must': {
                'bool': [
                    {
                        'match': {
                            variable.Variable(
                                'term', default=0
                            ): variable.Variable('value', default=0)
                        }
                    },
                ]
            }
        }

    q = RQuery()

    assert q.get_es_query({'term': 'x', 'value': 'y'})['aggs'] == {
        'must': {
            'bool': [
                {
                    'match': {
                        'x': 'y'
                    }
                }
            ]
        }
    }
