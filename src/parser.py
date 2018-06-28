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
    return schema


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
    returnedSchema = main('../records/')
    #pretend the below schema is what was returned by the above function
    #returnedSchema = {'contributors': {'schema': {'authors': {'schema': {'firstname': {'schema': {}, 'classes': {<class 'str'>}}, 'lastname': {'schema': {}, 'classes': {<class 'str'>}}}, 'classes': {<class 'list'>}}, 'test': {'schema': {}, 'classes': {<class 'str'>}}}, 'classes': set()}, 'date': {'schema': {'day': {'schema': {}, 'classes': {<class 'int'>}}, 'month': {'schema': {}, 'classes': {<class 'int'>}}, 'year': {'schema': {}, 'classes': {<class 'int'>}}}, 'classes': set()}, 'contents': {'schema': {}, 'classes': {<class 'str'>, <class 'int'>}}, 'publisher': {'schema': {}, 'classes': {<class 'str'>}}}
    print(returnedSchema)

    '''
    Notes:
    Key: * means the value is optional

            String | Integer | Float | Object | Array | Boolean | null
    String |       | String  | String| Array  | Array | Array   | String*
    Integer|String |         | Float | Array  | Array | Array   | Integer*
    Float  |String | Float   |       | Array  | Array | Array   | Float*
    Object |Array  | Array   | Array |        | Array | Array   | Object*
    Array  |Array  | Array   | Array | Array  |       | Array   | Array*
    Boolean|Array  | Array   | Array | Array  | Array |         | Boolean*
    null   |String*| Integer*| Float*| Object*| Array*| Boolean*| 

    '''

    #create a hash table like the one above
    table = {};
    #create the rows
    table["str"] = {"int": "str", "float": "str", "dict": "list", "list": "list", "bool": "list", "null": "str"}
    table["int"] = {"str": "str", "float": "float", "dict": "list", "list": "list", "bool": "list", "null": "int"}
    table["float"] = {"str": "str", "int": "float", "dict": "list", "list": "list", "bool": "list", "null": "float"}
    table["dict"] = {"str": "list", "int": "list", "float": "list", "list": "list", "bool": "list", "null": "dict"}
    table["list"] = {"str": "list", "int": "list", "float": "list", "dict": "list", "bool": "list", "null": "list"}
    table["bool"] = {"str": "list", "int": "list", "float": "list", "dict": "list", "list": "list", "null": "bool"}
    table["null"] = {"str": "str", "int": "int", "float": "float", "dict": "dict", "list": "list", "bool": "bool"}
