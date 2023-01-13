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
from devtools import debug

# File management
def to_json(filename, data):
    with open(filename, 'w+') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_lines(filename):
    with open(filename) as f:
        return f.read().split('\n')



# Parsing in place
def dismember_raw_verse(line: str) -> tuple[str, str, str]:
    """Splits the start and end tags from the verse text."""
    regex = r'(<verse osisID.+?/>)(.+?)(<verse eID.+?/>)'
    return tuple(filter(None, re.split(regex, line)))

def find_raw_tagged_words(line: str) -> list[str]:
    """Finds tagged words in a verses data protion."""
    words = re.findall(r'<w.+?/*>.+?</w>', line)
    return words or ['']

def parse_verseline_as_pair(
    line: str,
) -> tuple[str, list[str]]:
    """Parses a verse into a tuple of the verse tag and the words."""
    dismembered = dismember_raw_verse(line)
    tagged_words = find_raw_tagged_words(dismembered[1])
    return (dismembered[0], tagged_words)

def parse_multiple_verselines(
    lines: list[str],
) -> dict[str, list[str]]:
    """Parses a verses array into a dict of raw containers."""
    verse_pairs = [parse_verseline_as_pair(line) for line in lines]
    return dict(verse_pairs)

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
