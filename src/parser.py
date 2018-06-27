import os
import json


def main(records_dir):
    final_paths = {}

    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith(".json"):
            with open(path) as f:
                data = json.load(f)
            traverse_dict(data, "", final_paths)

    for key in final_paths:
        print(key + ": ", end="")
        for item in final_paths[key]:
            print(item, end="")
            print(", ", end="")
        print()


def traverse(obj, path, all_paths):
    if type(obj) is dict:
        traverse_dict(obj, path, all_paths)
    elif type(obj) is list:
        traverse_list(obj, path, all_paths)
    else:
        traverse_other(obj, path, all_paths)


def traverse_dict(d, path, all_paths):
    for key in d:
        traverse(d[key], (path + key + "/"), all_paths)


def traverse_list(l, path, all_paths):
    for item in l:
        traverse(item, path, all_paths)


def traverse_other(o, path, all_paths):
    if path in all_paths:
        all_paths[path].add(type(o))
    else:
        all_paths[path] = {type(o)}


if __name__ == '__main__':
    main('../records/')
