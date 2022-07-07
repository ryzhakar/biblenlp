"""This script targets building a json structure book-chapter-verse-originalwords.

Other information is somewhat preserved, if not explicitly discarded.
Inner verse structure besides the original words is lost

Some of the functions below are reusable.
"""

import json
import re
from typing import Any, Mapping, Sequence, Union


# File management
def to_json(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
def load_lines(filename):
    with open(filename, 'r') as f:
        return f.read().split('\n')


# Filtering
def starts_with_tags(line: str, tags: Sequence[str]) -> bool:

    if len(tags) > 1:
        tags = '|'.join(tags)
    else:
        tags = tags[0]

    return re.match(fr'\s*</*({tags})', line) is not None

def except_stuff(line: str):
    stuff = [
        '<div type="colophon"'
    ]
    return any(line.startswith(x) for x in stuff)


def specific_filtering(line: str, tags: Sequence[str]) -> bool:
    """Combines starts_with_tags and except_stuff"""

    return starts_with_tags(line, tags) and not except_stuff(line)

def filter_lines(
    tags: Sequence[str],
    lines: Sequence[str],
    filter_method
    ) -> Sequence[str]:
    """Leaves only lines that start with specified tags"""
    
    return [line for line in lines if filter_method(line, tags)]


# Parsing in place
def separate_verse(line: str) -> Sequence[str]:
    """Returns a list of <verse> tags and their contents"""
    return [
        x
        for x in re.split(r'(<verse osisID.+?/>)(.+?)(<verse eID.+?/>)', line)
        if x
        ]

def separate_original_words(line: str) -> Sequence[Sequence[str]]:
    """Returns a tuple of lists of original words and of everything else"""
    words = re.findall(r'<w.+?/*>.+?</w>', line)
    
    # Other info in the verses can be retained,
    # but changes structure of the file
    # stuff = re.split(r'<w.+?/*>.+?</w>', line)
    # return (words, stuff)
    if not words:
        return ['',]

    return words

def parse_verses(lines: Sequence[str]) -> Sequence[dict]:
    """Parses a verse into a dict"""
    w_sep_tags = [separate_verse(line) for line in lines]
    named_array_words = [
        {tg[0]: separate_original_words(tg[1])}
        for tg in w_sep_tags
    ]
    return named_array_words




# Structuring
def build_raw_structure(
    tags: Sequence[str],
    lines: Sequence[str],
    deepest_level_method,
    ) -> Sequence[Any]:
    """Constructs a list of dicts with tag lines as keys and other lines as values"""
    layer = []
    tagline = ''
    if not tags:
        return deepest_level_method(lines)
    
    for line in lines:
        if line.lstrip().startswith(f'<{tags[0]}'):
            tagline = line
            layer.append({tagline: list()})
        elif line.lstrip().startswith(f'</{tags[0]}'):
            layer[-1][tagline] = build_raw_structure(tags[1:], layer[-1][tagline], deepest_level_method)
        else:
            layer[-1][tagline].append(line)
    return layer

def unify_structure(structure: Sequence[dict]) -> Union[Mapping, Sequence]:
    """Unifies the structure of a list of dicts"""
    
    
    if isinstance(structure[0], dict):
        unified = dict()
        for d in structure:
            key = list(d.keys())[0]
            value = d[key]
            unified[key] = unify_structure(value)
        return unified
    else:
        return structure



# Main function
def untangle_osis(file_wo_ext: str):
    lines = load_lines(f'{file_wo_ext}.xml')
    lines = filter_lines(['div', 'chapter', 'verse'], lines, specific_filtering)
    layers = build_raw_structure(['div', 'chapter'], lines, parse_verses)
    layers = unify_structure(layers)
    return layers



if __name__ == "__main__":
    pass
    #file_wo_ext = input('Enter the file name without extension: ')
    #to_json(f'{file_wo_ext}.json', untangle_osis(file_wo_ext))
