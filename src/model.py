import utils
from functools import reduce


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
        if self.record:
            for key in self.record:
                if type(key) is str:
                    s += f"'{key}'"
                else:
                    s += str(key)
                s += f': {self.record[key]}, '
            s = s[:-2]
        s += '}'
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
        self.classes = set()
        records = []
        for t in types:
            if type(t) is Record:
                records.append(t)
            else:
                self.classes.add(t)

        self.record = Record({})
        if records:
            def reduce_fuse(r1, r2):
                r1.fuse(r2)
                return r1
            self.record = reduce(reduce_fuse, records)

    # def contains(self, t):
    #     return t in self.types

    def add(self, t):
        if type(t) is Record:
            self.record.fuse(t)
        else:
            self.classes.add(t)

    def __str__(self):
        s = ''
        if self.classes:
            s += ' + '.join([str(t) for t in self.classes])
            if self.record.record:
                s += ' + '
        if self.record.record:
            s += str(self.record)
        return s
