import model


def parser_type(o):
    if str(type(o))[8:].startswith('model'):
        return o
    elif type(o) is dict:
        return model.Record(o)
    elif type(o) is list:
        # TODO
        pass
    else:
        return model.Atom(o)
