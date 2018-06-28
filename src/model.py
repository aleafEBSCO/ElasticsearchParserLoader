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

    def __hash__(self):
        return hash(self.type)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.type == other.type

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

    def fuse(self, other):
        """Fuse this Record with another."""
        # TODO: Issues arise when fusing because sometimes nested Records appear
        # as Record objects and other times they're still simply dicts
        d = other.record
        for key in d:
            if key in self.record:
                if type(self.record[key]) is Union:
                    self.record[key].add(d[key])
                else:
                    self.record[key] = Union([self.record[key], d[key]])
            else:
                self.record[key] = d[key]

    def __hash__(self):
        return hash(repr(self.record))

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.record == other.record

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


class Array:
    """Represents array types."""

    def __init__(self, val):
        types = set([utils.parser_type(v) for v in val])
        self.array_type = Union(types)

    def __str__(self):
        return f'[({self.array_type})*]'


class Union:
    """Represents a union of multiple types of data.
    Example: <class 'int'> + <class 'str'> + {'hello': <class 'bool'>}
    """

    def __init__(self, types):
        self.types = list(types)

    def contains(self, t):
        return t in self.types

    def add(self, t):
        if t not in self.types:
            self.types.append(t)

    def __str__(self):
        return ' + '.join([str(t) for t in self.types])
