
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


def generate_query_docs(q, _filter=None):
    """
    Return a full description of a the query to create the documentation.
    """
    _docs_template.format(
        id=q.get_id(),
        name=q.name,
        long_description=q.__doc__,
        query='\n  '.join(json.dumps(q.full_query,
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
