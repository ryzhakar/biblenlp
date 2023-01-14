import json


def to_json(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_lines(filename):
    with open(filename) as f:
        return f.read().split('\n')
