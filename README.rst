.. image:: https://travis-ci.org/openshine/python-esqb.svg?branch=master
    :target: https://travis-ci.org/openshine/python-esqb

===========================
ElasticSearch Query Builder
===========================

A Query Builder to build queries specially suited for ElasticSearch queries

Examples
--------

Basic example
+++++++++++++

This code show how to define a simple query.

.. code-block:: python

    from esqb.query import BaseQuery


    class SimpleQuery():
        size = 0
        query = {
            "bool": {
                "must": [
                    {
                        "term": {
                            "name": {
                                "value": "esqb"
                            }
                        }
                    }
                ]
            }
        }
        aggs = {
            "by_logtime": {
                "date_histogram": {
                    "field": "time",
                    "interval": "day",
                    "order": {
                        "_key": "desc"
                    }
                }
            }
        }

and this is the generated query.

.. code-block:: json

    {
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "name": {
                  "value": "esqb"
                }
              }
            }
          ]
        }
      },
      "size": 0,
      "aggs": {
        "by_logtime": {
          "date_histogram": {
            "field": "time",
            "interval": "day",
            "order": {
              "_key": "desc"
            }
          }
        }
      },
      "sort": []
    }

Variables and filters
+++++++++++++++++++++

Example to create a query to show the the last **N** documents ordered by a **sort_field** between two dates (**ts** and **te**)

v.py
^^^^

This file show how to define the query variables.

.. code-block:: python

    from esqb.variable import Variable


    ts = Variable('ts', None, str, True, 'Time start')
    te = Variable('te', '2017-12-01', str, True, 'Time end')
    size = Variable('query_size', 10, str, False, 'Term size')
    sort_field = Variable('sort_field', '', str, True,
                          'Field to do the ordination')
    sort_order = Variable('sort_order', '', str, True, 'asc or desc')
    variables = {
        v.name: v.name for v in [
            ts,
            te,
            size,
            sort_field,
            sort_order
        ]
    }

filters.py
^^^^^^^^^^

This file show how to define a esqb query filter to add a date range.

.. code-block:: python

    from esqb.queryfilter import QueryFilter


    class time_range_filter(QueryFilter):
        """
        Query filter to filter between two dates.
        """

        def __init__(self, field, ts, te):
            self.field = field
            self.variables = {
                'ts': ts,
                'te': te,
            }

        def apply(self, query, data):
            query.setdefault(
                'bool', {}
            ).setdefault(
                'must', []
            ).append(
                {
                    'range': {
                        self.field: {
                            'gte': self.variables['ts'],
                            'lte': self.variables['te'],
                        }
                    }
                }
            )
            return query

last_docs.py
^^^^^^^^^^^^

This file show how to define a parameterized elasticsearch query using the filters and variables previously defined.

.. code-block:: python

    from esqb.query import BaseQuery
    from filters import time_range_filter
    from v import (
        size,
        sort_field,
        sort_order,
        ts,
        te
    )


    class LastDocs(BaseQuery):

        size = size
        sort = [
            {
                sort_field: {
                    "unmapped_type": "float",
                    "missing": "_last",
                    "order": sort_order
                }
            }
        ]

        def __init__(self):
            BaseQuery.__init__(self)
            self.filters = [
                time_range_filter('timestamp', ts, te)
            ]

        def result(self, response):
            return [r.get('_source', {}) for r in self.dotget(response, 'hits.hits')]


    __doc__ = LastDocs().docs(variables)

example.py
^^^^^^^^^^

This file show how to create a complete query ready to be used by elasticsearch.

.. code-block:: python

    from last_docs import LastDocs


    if __name__ == '__main__':
        q = LastDocs().get_es_query(
            {
                'ts': '1980',
                'te': '1990',
                'query_size': 3,
                'sort_order': 'asc',
                'sort_field': 'age'
            }
        )
        print(q)

And this is the query.

.. code-block:: sh

    $> python example.py

    {
      "query": {
        "bool": {
          "must": [
            {
              "range": {
                "timestamp": {
                  "gte": "1980",
                  "lte": "1990"
                }
              }
            }
          ]
        }
      },
      "size": 3,
      "aggs": {},
      "sort": [
        {
          "age": {
            "unmapped_type": "float",
            "missing": "_last",
            "order": "asc"
          }
        }
      ]
    }


Features
--------

* TODO

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
