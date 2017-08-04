=====
Usage
=====

The ElasticSearch Query Builder has three main components: Queries, QueryFilters and Variables.

In order to use them, you need to import::

  from esqb.query import BaseQuery
  from esqb.queryfilter import QueryFilter
  from esqb.variable import Variable

There is also Django REST Framework support, which allows you to
automatically synthetize serializers. The DRF serializers support can be imported by::

  import esqb.drf_support



