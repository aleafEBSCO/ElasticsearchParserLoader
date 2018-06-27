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

    # schema = accumulate_schema(data)
    schema = compute_schema(data[0])
    pprint(schema)


# Compute the schema for a single dictionary
def compute_schema(d):
    # When encoding a dictionary to the schema, all the keys are added and all
    # the value types are put into a new or existing set
    schema = {}
    for key in d:
        new_type = parser_type(d[key])

        # New key -> type set must be created
        if key not in schema:
            schema[key] = [new_type]
        # Only add new type if it isn't already there
        elif new_type not in schema[key]:
            schema[key].append(new_type)
    return schema


def parser_type(o):
    if type(o) is dict:
        return compute_schema(o)
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
