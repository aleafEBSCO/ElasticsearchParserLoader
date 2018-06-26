import os
import json


def main(records_dir):
    final_paths = {}

    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith(".json"):
            with open(path) as f:
                data = json.load(f)
            traverse(data, "", final_paths)

    for key in final_paths:
        print(key + ": ", end="")
        for item in final_paths[key]:
            print(item, end="")
            print(", ", end="")
        print()


def traverse(obj, path, all_paths):
    if type(obj) is not dict:
        if type(obj) is list:
            for item in obj:
                if type(item) is dict:
                    for key in item.keys():
                        traverse(item[key], (path + key + "/"), all_paths)
                else:
                    if path in all_paths:
                        all_paths[path].add(type(item))
                    else:
                        all_paths[path] = {type(item)}

                    # print(curPath + ": ", end="")
                    # print(type(obj))
        else:
            if path in all_paths:
                all_paths[path].add(type(obj))
            else:
                all_paths[path] = {type(obj)}
            # print(curPath + ": ", end="")
            # print(type(obj))
    else:
        for key in obj.keys():
            traverse(obj[key], (path + key + "/"), all_paths)

    return all_paths


if __name__ == '__main__':
    main('../records/')
