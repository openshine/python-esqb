import os
import sys
from copy import deepcopy

from .variable import Variable
from .utils import replace_variables as _replace_variables


class BaseQuery(object):
    """
    This object contains everything necessary to create serializers
    from queries. This object resolves variables in queries as well as
    possible filters (optional or required) which may change the final
    query to be given to ES.

    """

    def __init__(self):
        """
        We make this arcane magic here so that we can have several
        instances of the same query and their base (class-based)
        attributes will not change if modified (because there is a
        copy in the instance).

        The serializer field exists to cache a serializer once it has
        been generated.

        """
        self._size = self.__class__.__dict__.get('size', 0)
        self._aggs = deepcopy(self.__class__.__dict__.get('aggs', {}))
        self._query = deepcopy(self.__class__.__dict__.get('query', {}))
        self.filters = deepcopy(self.__class__.__dict__.get('filters', []))
        self._sort = deepcopy(self.__class__.__dict__.get('sort', []))
        self._serializer = None

    def get_id(self):
        """
        TODO: Probably just return self.__class__.__module__
        """
        fullpath = sys.modules[self.__class__.__module__].__file__
        name = os.path.basename(fullpath)
        dot = name.rfind('.')
        return (name[:dot], fullpath)

    @property
    def aggs(self):
        """
        Returns the ``aggs`` property of the query.
        """
        return self._aggs

    @aggs.setter
    def aggs(self, val: dict):
        self._aggs = val

    @property
    def query(self):
        """
        Returns the ``query`` property of the query.
        """
        return self._query

    @query.setter
    def query(self, val: dict):
        self._query = val

    @property
    def size(self):
        """
        Returns the ``size`` property of the query.
        """
        return self._size

    @size.setter
    def size(self, val):
        self._size = val

    @property
    def sort(self):
        """
        Returns the ``sort`` property of the query.
        """
        return self._sort

    @sort.setter
    def sort(self, val):
        self._sort = val

    def get_es_query(self, data: dict) -> dict:
        """
        Return the final ES query that should be presented to ESService.

        This function scans variables and fills their values with the
        provided arg `data`.
        """
        _vars = {}
        for var in self.find_all_variables():
            _vars[var.name] = var

        return {_q: _replace_variables(self._filtered(_q, data), data)
                for _q in ('query', 'size', 'aggs', 'sort')}

    def _filtered(self, query_field, data: dict) -> dict:
        """Filters the query parts with the defined query filters"""
        d = deepcopy(getattr(self, query_field))
        for _filter in self.filters:
            if _filter.query_field == query_field:
                d = _filter(d, data)
        return d

    @property
    def serializer(self, **kwargs):
        """
        Creates a serializer instance and returns such an instance on
        following calls.

        """
        if not self._serializer:
            self._serializer = self.get_serializer()(**kwargs)
        return self._serializer

    @serializer.setter
    def serializer(self, value):
        self._serializer = value

    def get_serializer(self):
        """
        You should use the utility function in drf_support so that
        this module becomes drf_free.
        """
        import warnings
        warnings.warn("Query.get_serialiser is deprecated. " +
                      "Use drf_support.get_query_serializer instead(query)",
                      DeprecationWarning)
        from . import drf_support
        return drf_support.get_query_serializer(self)

    def find_all_variables(self, docs=None, prev=None, include_filters=True):
        """
        Returns all variables found in the query and its filters
        """
        if docs is None:
            prev = [] if not include_filters else [
                var
                for _filter in self.filters
                for var in _filter.get_variables().values() if include_filters
            ]
            return self.find_all_variables(
                [self.query, self.aggs, self.size, self.sort], prev
            )

        if type(docs) is list:
            for elt in docs:
                if type(elt) is Variable:
                    prev.append(elt)
                else:
                    self.find_all_variables(elt, prev)
        elif type(docs) is dict:
            for k, v in docs.items():
                if type(k) is Variable:
                    prev.append(k)
                if type(v) is Variable:
                    prev.append(v)
                else:
                    self.find_all_variables(v, prev)
        return prev

    def dotget(self, doc: dict, path: str):
        """
        Utility function to navigate paths using dot-notation.
        """
        for key in path.split('.'):
            doc = doc[key]
        return doc

    @property
    def name(self):
        """
        Unless overwritten, the name is the class name
        """
        return self.__class__.__name__

    @property
    def full_query(self):
        """
        Returns the query as it would be compiled to be sent to
        ElasticSearch.

        Writing to this property is not supported at the
        moment. Please use ``aggs`` and ``query``.

        """
        return {
            'size': self.size,
            'query': self.query,
            'aggs': self.aggs,
            'sort': self.sort
        }

    def docs(self, variables):
        """
        Returns the documentation of this query.

        This method is deprecated, please use
        :func:`esqb.docs_builder.generate_query_docs`

        """
        import warnings
        warnings.warn('query.docs is deprecated. ' +
                      'Use docs_builder.generate_query_docs(query)',
                      DeprecationWarning)
        from .docs_builder import generate_query_docs
        return generate_query_docs(self, variables)

    def view_docs(self, variables):
        """
        Returns the view documentation of this query.

        This method is deprecated, please use
        :func:`esqb.docs_builder.generate_view_docs`

        """
        import warnings
        warnings.warn('query.docs is deprecated. ' +
                      'Use docs_builder.generate_view_docs(query)',
                      DeprecationWarning)
        from .docs_builder import generate_view_docs
        return generate_view_docs(self, variables)
