"""This script targets building a json structure book-chapter-verse-
originalwords.

Other information is somewhat preserved, if not explicitly discarded.
Inner verse structure besides the original words is lost

Some of the functions below are reusable.
"""
import json
import re
from collections.abc import Mapping
from collections.abc import Sequence
from typing import Any

from .filter_functions import filter_lines
from .filter_functions import starts_with_whitelisted


# File management
def to_json(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_lines(filename):
    with open(filename) as f:
        return f.read().split('\n')



# Parsing in place
def separate_verse(line: str) -> list[str]:
    """Returns a list of <verse> tags and their contents."""
    regex = r'(<verse osisID.+?/>)(.+?)(<verse eID.+?/>)'
    return list(filter(None, re.split(regex, line)))

def separate_original_words(line: str) -> Sequence[Sequence[str]]:
    """Returns a tuple of lists of original words and of everything else."""
    words = re.findall(r'<w.+?/*>.+?</w>', line)

    # Other info in the verses can be retained,
    # but changes structure of the file
    # stuff = re.split(r'<w.+?/*>.+?</w>', line)
    # return (words, stuff)
    if not words:
        return ['']

    return words

def parse_verses(lines: Sequence[str]) -> Sequence[dict]:
    """Parses a verse into a dict."""
    w_sep_tags = [separate_verse(line) for line in lines]
    named_array_words = [
        {tg[0]: separate_original_words(tg[1])}
        for tg in w_sep_tags
    ]
    return named_array_words


# Structuring
def build_raw_structure(
    tags: list[str],
    lines: list[str],
    deepest_level_method,
) -> Sequence[Any]:
    """Constructs a list of dicts with tag lines as keys and other lines as
    values."""
    layer: list[dict[str, str]] = []
    tagline = ''
    if not tags:
        return deepest_level_method(lines)

    for line in lines:
        if line.lstrip().startswith(f'<{tags[0]}'):
            tagline = line
            layer.append({tagline: []})
        elif line.lstrip().startswith(f'</{tags[0]}'):
            layer[-1][tagline] = build_raw_structure(
                tags[1:], layer[-1][tagline], deepest_level_method,
            )
        else:
            layer[-1][tagline].append(line)
    return layer


def unify_structure(structure: Sequence[dict]) -> Mapping | Sequence:
    """Unifies the structure of a list of dicts."""

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
def untangle_osis(filename: str):
    lines = load_lines(filename)
    lines = filter_lines(
        ['div', 'chapter', 'verse'],
        lines, starts_with_whitelisted,
    )
    layers = build_raw_structure(['div', 'chapter'], lines, parse_verses)
    layers = unify_structure(layers)
    return layers
