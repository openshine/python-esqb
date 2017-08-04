from es_query_builder.drf_support import _default_variable_serializers


__all__ = ['Variable']


class Variable(object):
    """A Variable is an element to be embedded in a query.  The variable
    can have a default value (if it is not required), and it has a
    help text, as well as a type. From this variable, a DRF serializer
    can be constructed. The serializer class can be automatically
    selected, but may be overridden in the cosntructor, as well as
    further parameters.
    """
    def __init__(self, name,
                 default=None,
                 type=int,
                 required=False,
                 help_text='Unknown variable',
                 serializer_class=None,
                 serializer_options=None,
                 ):
        self.name = name
        self.default = default
        self.type = type
        self.required = required
        self.help_text = help_text
        self.serializer_options = serializer_options or {}
        self.serializer_class = serializer_class

    def copy(self, **kwargs):
        """
        Copy the variable, optionally changing some of the values.

        Implementation nodte: currently it uses the __dict__ of the
        object for the copy.
        """
        d = self.__dict__.copy()
        d.update(kwargs)
        return Variable(
            **d
        )

    def value_from_dict(self, d=None):
        """
        Returns the value of the variable given the received data.

        If no data matches this variable name, its default value is
        returned.

        """
        if d is None:
            d = {}
        if self.required and self.name not in d:
            raise Exception(
                "Required variable {} does not have a value".format(
                    self.name)
            )
        else:
            return d.get(self.name, self.default)

    def __str__(self):
        """
        Returns a formatted text of this variable as an explanation.
        """
        if self.required:
            return '${{{name}:?Required. {doc}}}'.format(
                name=self.name,
                doc=self.help_text,
            )
        else:
            return '${{{name}:-{default}:?{doc}}}'.format(
                name=self.name,
                default=self.default,
                doc=self.help_text,
            )

    def __repr__(self):
        """Returns a representation of the object for schematic purposes.
        (R) means required, (O) means optional."""
        return "<Var [{name} :: {type} = {default} {req}]>".format(
            name=self.name,
            type=self.type.__name__,
            default=repr(self.default),
            req="(R)" if self.required else "(O)"
        )
