import os
import json

from pprint import pprint


def main(records_dir):
    data = []
    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith('.json'):
            with open(path) as f:
                data.append(json.load(f))

    schema = {}
    for d in data:
        schema = compute_schema(d, schema)
    pprint(schema)


# Compute the overall schema given a current schema
def compute_schema(d, schema):
    # When encoding a dictionary to the schema, all the keys are added and all
    # the value types are put into a new or existing set
    for key in d:
        new_type = parser_type(d[key])
        if type(new_type) is dict:
            schema = add_schema(key, new_type, schema)
        else:
            schema = add_class(key, new_type, schema)
    return schema


def add_schema(key, s, schema):
    # TODO: Breaks if one value is schema and another is class
    # (everything may need to be a list after all...)
    schema[key] = s
    return schema


def add_class(key, c, schema):
    # New key -> type set must be created
    if key not in schema:
        schema[key] = [c]
    # Only add new type if it isn't already there
    elif c not in schema[key]:
        schema[key].append(c)
    return schema


def parser_type(o):
    if type(o) is dict:
        return compute_schema(o, {})
    else:
        return type(o)


# =================================================================
def accumulate_schema(data):
    schema = {}
    for d in data:
        traverse_dict_old(d, schema)
    return schema


def traverse(obj, schema):
    if type(obj) is dict:
        traverse_dict_old(obj, schema)
    elif type(obj) is list:
        traverse_list(obj, schema)


# TODO: Handle list types
def traverse_dict_old(d, schema):
    for key in d:
        # HACK: Type check for other here instead of in traverse to conserve
        # type in schema
        # If value of current key is a dict or list, extend schema
        if type(d[key]) in [dict]:  # , list]:
            schema[key] = dict()
            traverse(d[key], schema[key])
        # Otherwise, add the type to the schema
        else:
            if key not in schema:
                schema[key] = {type(d[key])}
            else:
                schema[key].add(type(d[key]))


def traverse_list(l, schema):
    for item in l:
        traverse(item, schema)


if __name__ == '__main__':
    main('../records/')
