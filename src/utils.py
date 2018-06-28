import model


def parser_type(o):
    if type(o) is dict:
        return model.Record(o)
    elif type(o) is list:
        # TODO
        pass
    else:
        return model.Atom(o)
