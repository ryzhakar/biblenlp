import re
from collections.abc import Iterable

from biblenlp.interface.types import RawBibleType
from biblenlp.parsing.file_io import load_lines
from biblenlp.parsing.filter_functions import filter_lines
from biblenlp.parsing.filter_functions import starts_with_whitelisted


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


def structure_from(
    *,
    stripped_xmlstr_sequence: Iterable[str],
) -> RawBibleType:
    """Structures a multilevel dict of raw strings from a sequence.

    Strictly depends on the order of the sequence.
    """
    # First two lines should be the book and chapter tags
    xml_iterator = iter(stripped_xmlstr_sequence)
    first_book_tag = next(xml_iterator)
    first_chapter_tag = next(xml_iterator)
    structure: RawBibleType = {
        first_book_tag: {
            first_chapter_tag: {},
        },
    }
    current_book = structure[first_book_tag]
    current_chapter = current_book[first_chapter_tag]
    div_tag = '<div'
    chapter_tag = '<chapter'
    verse_tag = '<verse'
    for line in xml_iterator:
        if line.startswith(div_tag):
            current_book = structure[line] = structure.get(line, {})
        elif line.startswith(chapter_tag):
            current_chapter = current_book[line] = current_book.get(line, {})
        elif line.startswith(verse_tag):
            verse, words = parse_verseline_as_pair(line)
            current_chapter[verse] = words
    return structure


def load_raw_structure_from(*, filename: str) -> RawBibleType:
    lines = load_lines(filename)
    filtered_lines_iterator = filter_lines(
        tags=['div', 'chapter', 'verse'],
        lines=lines,
        filter_method=starts_with_whitelisted,
    )
    return structure_from(stripped_xmlstr_sequence=filtered_lines_iterator)
