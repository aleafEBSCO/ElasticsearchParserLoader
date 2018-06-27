import os
import json

from pprint import pprint


def main(records_dir):
    # final_paths = dict()

    data = []
    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith('.json'):
            with open(path) as f:
                data.append(json.load(f))

    schema = compute_schema(data)

    # print('\n-----------------------------------')
    pprint(schema)
    # for key in final_paths:
    #     print(key + ': ', end='')
    #     for item in final_paths[key]:
    #         print(str(item) + ', ', end='')
    #     print()


def compute_schema(data):
    schema = {}
    for d in data:
        traverse_dict(d, schema)
    return schema


def traverse(obj, schema):
    if type(obj) is dict:
        traverse_dict(obj, schema)
    elif type(obj) is list:
        traverse_list(obj, schema)


def traverse_dict(d, schema):
    for key in d:
        # HACK: Type check for other here instead of in traverse to conserve type in schema
        # If value of current key is a dict or list, extend the schema and go deeper
        if type(d[key]) in [dict, list]:
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
