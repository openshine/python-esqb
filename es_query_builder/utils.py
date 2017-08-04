from .variable import Variable


def replace_variables(d, data: dict):
    """
    Replace variables in `d` (usually BaseQuery.query)
    with data from the `data` dict.
    """
    if type(d) is dict:
        d = d.copy()
        for k, v in d.items():
            if isinstance(v, Variable):
                d[k] = v.value_from_dict(data)
            else:
                d[k] = replace_variables(v, data)
    elif type(d) is list:
        d[:] = d
        for i, v in enumerate(d):
            if isinstance(v, Variable):
                d[i] = v.value_from_dict(data)
            else:
                d[i] = replace_variables(v, data)
    return d
