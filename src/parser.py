import os
import json
import model


def main(records_dir):
    data = []
    for filename in os.listdir(records_dir):
        path = records_dir + filename
        if path.endswith('.json'):
            with open(path) as f:
                data.append(json.load(f))

    schema = model.Record({})
    for d in data:
        schema.fuse(model.Record(d))
    print(schema)


if __name__ == '__main__':
    main('../records/')
