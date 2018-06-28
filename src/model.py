import utils


class Atom:
    """Represents atomic types.
    Examples: str, int, bool
    """

    def __init__(self, val):
        if type(val) not in [list, dict]:
            self.type = type(val)
        else:
            raise TypeError

    def __str__(self):
        return str(self.type)


class Record:
    """Represents record types as dicts."""

    def __init__(self, val):
        if type(val) is dict:
            self.record = dict()
            for key in val:
                self.record[key] = utils.parser_type(val[key])
        else:
            raise TypeError

    def __str__(self):
        s = '{'
        for key in self.record:
            if type(key) is str:
                s += f"'{key}'"
            else:
                s += str(key)
            s += f': {self.record[key]}, '
        s = s[:-2] + '}'
        return s

# TODO: Implement array types


class Union:
    """Represents a union of multiple types of data.
    Example: <class 'int'> + <class 'str'> + {'hello': <class 'bool'>}
    """

    def __init__(self, types):
        self.types = types

    def __str__(self):
        return ' + '.join([str(t) for t in self.types])
