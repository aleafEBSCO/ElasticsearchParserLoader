import os
import json

directory = os.fsencode("../records")
for file in os.listdir(directory):
    filename = os.fsdecode(file)

    openFile = "../records" + "/" + filename
    if openFile.endswith(".json"):
        with open(openFile) as f:
            data = json.load(f)
        print(data['contents'])
        

