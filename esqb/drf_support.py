import collections

from django.core.exceptions import ImproperlyConfigured
try:
    from rest_framework import serializers
except ImproperlyConfigured:
    import os
    import warnings
    warnings.warn("""Django settings not detected.
You should use drf_support inside a Django application.
Continuing with an empty DJANGO_SETTINGS_MODULE
""")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'x')
    from rest_framework import serializers
from rest_framework.utils import html


def get_variable_serializer_field(variable):
    """"
    Returns a serializer field for a variable.

    The variable MAY add parameters to the serializer via a
    serializer_field_options property.

    """
    if hasattr(variable, 'serializer_field_options'):
        sfo = variable.serializer_field_options or {}
    else:
        sfo = {}

    sfo.setdefault('required', variable.required)
    if not variable.required and variable.default:
        sfo['default'] = variable.default
    elif 'default' in sfo:
        del sfo['default']

    return get_variable_serializer_field_class(variable)(
        help_text=variable.help_text, **sfo)


def get_variable_serializer_field_class(variable):
    """
    Usually, you should not worry about this and use
    get_query_serializer directly.

    But you may add a variable.serializer_class parameter if you wish
    to customize the serializer field that your variable outputs.

    """
    if hasattr(variable, 'serializer_field_class') and \
       variable.serializer_field_class:
        return variable.serializer_field_class

    return _default_variable_serializers[variable.type]


def get_query_serializer(query, hide=()):
    """Creates a serializer synthetically with parameters defined by all
    the variables defined in the query and its available filters.

    You can avoid pushing variables to the serializer if you
    include them (either strings containing their names or the
    objects themselves) in the optional hide parameter.

    """
    name = "Synthetic" + query.get_id()[0] + "Serializer"
    params = {
        var.name: get_variable_serializer_field(var)
        for var in query.find_all_variables()
        if var not in hide and var.name not in hide
    }
    return type(name, (serializers.Serializer, ), params)


class ListField(serializers.ListField):
    def to_internal_value(self, data):
        """
        List of dicts of native values <- List of dicts of primitive datatypes.
        """
        _data = data[0].split(',') if len(data) > 0 else data
        if html.is_html_input(_data):
            data = html.parse_html_list(_data)
        if isinstance(_data, type('')) or \
           isinstance(_data, collections.Mapping) or \
           not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(_data).__name__)
        if not self.allow_empty and len(_data) == 0:
            self.fail('empty')
        return [self.child.run_validation(item) for item in _data]


_default_variable_serializers = {
    int: serializers.IntegerField,
    float: serializers.FloatField,
    str: serializers.CharField,
    bool: serializers.BooleanField,
    list: ListField
}
