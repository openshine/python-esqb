import json

from .variable import Variable

__all__ = ['generate_query_docs']

_docs_template = """
* **ID**: ``{id}``
* **name**: ``{name}``

{long_description}

.. code-block:: json

  {query}
"""

_view_template = """

* **Query**:

.. code-block:: json

    {query}

    """


def generate_query_docs(q, variables=None):
    """
    Return a full description of a the query to create the documentation.
    """
    return _docs_template.format(
        id=q.get_id(),
        name=q.name,
        long_description=q.__doc__ or '',
        query='\n  '.join(
            json.dumps(
                q.get_es_query(variables or {}),
                indent=2,
                default=_explaining_json_encoder,
                sort_keys=True).split('\n')))


def generate_view_docs(q, variables=None):
    """
    Return a simple description of a the query to create the view documentation.
    """
    return _view_template.format(
            query='\n  '.join(
                json.dumps(
                    q.get_es_query(variables or {}),
                    indent=2,
                    default=_explaining_json_encoder,
                    sort_keys=True).split('\n')))


def _explaining_json_encoder(obj):
    """
    A JSON encoder which understands Variables.
    """
    if isinstance(obj, Variable):
        return str(obj)
    else:
        return obj
