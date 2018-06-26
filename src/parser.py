import os
import json


def recurseObject(obj, curPath, paths):
    if type(obj) is not dict:
        if type(obj) is list:
            for item in obj:
                if type(item) is dict:
                    for key in item.keys():
                        recurseObject(item[key], (curPath + key + "/"), paths)
                else:
                    if curPath in paths:
                        paths[curPath].add(type(item))
                    else:
                        paths[curPath] = set([type(item)])

                    #print(curPath + ": ", end="")
                    #print(type(obj))
        else:
            if curPath in paths:
                paths[curPath].add(type(obj))
            else:
                paths[curPath] = set([type(obj)])
            #print(curPath + ": ", end="")
            #print(type(obj))
    else:
        for key in obj.keys():
            recurseObject(obj[key], (curPath + key + "/"), paths)

    return paths


finalPaths = dict();

for filename in os.listdir("../records"):

    openFile = "../records" + "/" + filename
    if openFile.endswith(".json"):
        with open(openFile) as f:
            data = json.load(f)
        recurseObject(data, "", finalPaths)
        #print(data['contents'])

for key in finalPaths.keys():
    print(key + ": ", end="")
    for item in finalPaths[key]:
        print(item, end="")
        print(", ", end="")
    print()
