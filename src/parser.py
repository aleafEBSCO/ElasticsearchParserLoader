import os
import json

from pprint import pprint


def main(records_dir):
    # final_paths = dict()
    schema = dict()

    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith('.json'):
            with open(path) as f:
                data = json.load(f)
            print('Traversing', filename)
            pprint(schema)
            traverse_dict(data, schema)

    print('\n-----------------------------------')
    pprint(schema)
    # for key in final_paths:
    #     print(key + ': ', end='')
    #     for item in final_paths[key]:
    #         print(str(item) + ', ', end='')
    #     print()


def traverse(obj, schema):
    if type(obj) is dict:
        traverse_dict(obj, schema)
    elif type(obj) is list:
        traverse_list(obj, schema)
    else:
        # schema = set()
        traverse_other(obj, schema)


def traverse_dict(d, schema):
    for key in d:
        if key not in schema:
            schema[key] = dict()
        traverse(d[key], schema[key])


def traverse_list(l, schema):
    for item in l:
        traverse(item, schema)


def traverse_other(o, schema):
    if type(o) in schema:
        schema[type(o)] += 1
    else:
        schema[type(o)] = 1


if __name__ == '__main__':
    main('../records/')
