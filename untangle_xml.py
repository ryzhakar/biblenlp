import json
from typing import Any, Sequence


def to_json(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
def load_lines(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')

def write_lines(filename, lines):
    with open(filename, 'w+') as f:
        f.write('\n'.join(lines))



def starts_with_tag(line: str, tags: Sequence[str]) -> bool:

    open = [
        line.startswith(f'<{tg}') or line.startswith(f'</{tg}')
        for tg in tags
    ]
    return any(open)

def filter_lines(tags: Sequence[str], lines: Sequence[str], filter_func):
    """Leaves only lines that start with specified tags"""
    
    return [line for line in lines if filter_func(line, tags)]

def build_structure(tags: Sequence[str], lines: Sequence[str]) -> Sequence[Any]:
    """Constructs a list of dicts with tag lines as keys and other lines as values"""
    layer = []
    tagline = ''
    if not tags:
        return lines
    
    for line in lines:
        if line.lstrip().startswith(f'<{tags[0]}'):
            tagline = line
            layer.append({tagline: list()})
        elif line.lstrip().startswith(f'</{tags[0]}'):
            layer[-1][tagline] = build_structure(tags[1:], layer[-1][tagline])
        else:
            layer[-1][tagline].append(line)
    return layer




if __name__ == "__main__":
    lines = load_lines('kjv.xml')
    lines = filter_lines(lines, ['div', 'chapter', 'verse'], starts_with_tag)
    layers = build_structure(['div', 'chapter'], lines)
    to_json('kjv.json', layers)