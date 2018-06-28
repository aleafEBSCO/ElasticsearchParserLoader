class Atom:
    """Represents atomic types.
    Examples: str, int, bool
    """

    def __init__(self, val):
        if type(val) not in [list, dict]:
            self.val = val
        else:
            raise TypeError


class Record:
    """Represents record types as dicts."""

    def __init__(self, val):
        if type(val) is dict:
            self.val = val
        else:
            raise TypeError


class Array:
    """Represents array types as lists."""

    def __init__(self, val):
        if type(val) is list:
            self.val = val
        else:
            raise TypeError
