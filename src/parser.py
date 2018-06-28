import os
import json
import model

# from pprint import pprint


def main(records_dir):
    data = []
    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith('.json'):
            with open(path) as f:
                data.append(json.load(f))

    # schema = {}
    # for d in data:
    #     schema = compute_schema(d, schema)
    # pprint(schema)

    schema = model.Record({})
    for d in data:
        schema.fuse(model.Record(d))
    print(schema)


# Compute the overall schema given a current schema
def compute_schema(d, schema):
    for key in d:
        new_type = parser_type(d[key])
        if type(new_type) is dict:
            add_schema(new_type, schema, key, d)
        else:
            add_class(new_type, schema, key)
    return schema


def add_schema(new_type, schema, key, d):
    # TODO: Could probably be futher refactored (see schema[key] and d[key])
    if key not in schema:
        schema[key] = {'schema': new_type, 'classes': set()}
    else:
        schema[key]['schema'] = compute_schema(d[key], schema[key]['schema'])


def add_class(new_type, schema, key):
    if key not in schema:
        schema[key] = {'schema': dict(), 'classes': {new_type}}
    else:
        schema[key]['classes'].add(new_type)


def parser_type(o):
    if type(o) is dict:
        return compute_schema(o, {})
    else:
        return type(o)


if __name__ == '__main__':
    main('../records/')
