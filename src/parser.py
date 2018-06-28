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
    for key in d:
        new_type = parser_type(d[key])
        if key not in schema:
            if type(new_type) is dict:
                schema[key] = {'schema': new_type, 'classes': set()}
            else:
                schema[key] = {'schema': dict(), 'classes': {new_type}}
        else:
            if type(new_type) is dict:
                schema[key]['schema'] = compute_schema(d[key], schema[key]['schema'])
            else:
                schema[key]['classes'].add(new_type)
    return schema


def parser_type(o):
    if type(o) is dict:
        return compute_schema(o, {})
    else:
        return type(o)


if __name__ == '__main__':
    main('../records/')
