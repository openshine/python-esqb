class QueryFilter(object):
    """
    A QueryFilter is an object that can be used in a query to restrict
    appearances of certain elements.

    Usually, a QueryFilter will override the `apply()` method and will
    change the received query into what's needed to filter further. As
    such, a filter exports a variables dictionary, with additional
    data which may (or must) be received from the API call. A filter
    may be required or optional (optional filters makes all its
    variables optional).
    """

    _variables = {}
    required = False

    def __call__(self, query, data={}):
        """
        A filter is callable this way. Receives the query (which can be
        mutated) and the data from forms or otherwise.
        """
        if self.can_apply(data):
            return self.apply(query)
        else:
            if self.required:
                raise Exception(
                    'Filter {} is required but variables were missing.'.format(
                        self.__name__
                    )
                )
            return query

    @property
    def variables(self):
        if self.required:
            return {
                k: variable.copy()
                for k, variable in self._variables.items()
            }
        else:
            return {
                k: variable.copy(required=False)
                for k, variable in self._variables.items()
            }

    @variables.setter
    def variables(self, value):
        self._variables = value

    def can_apply(self, data):
        """
        Whether we can apply the filter, notwithstanding its required property.

        A filter can be applied if all its required variables are found in
        `data`.

        """

        for k, v in self._variables.items():
            if v.name not in data:
                return False
        return True

    def apply(self, query):
        """
        Override this function in your filter so that it does something.
        """
        return query

