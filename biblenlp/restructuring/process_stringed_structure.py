from collections.abc import Sequence

from bs4 import BeautifulSoup

from biblenlp.interface.models import Bible
from biblenlp.interface.models import Book
from biblenlp.interface.models import Chapter
from biblenlp.interface.models import Verse
from biblenlp.interface.models import Word


def read_all_xml_tags(xml_string: str):
    soup = BeautifulSoup(xml_string, 'xml')
    return list(soup.find_all())


def get_split(dictionary: dict, key: str) -> list:
    """Returns a list of values for a given key in a dictionary."""
    value = dictionary.get(key)
    if value is None:
        return []
    else:
        return value.split(' ')


def parse_from_xml_str_word(xml_string: str) -> Word:
    """Restructures a single XML <w> tag into a Word object."""
    soup = read_all_xml_tags(xml_string)
    text = soup[0].text
    attrs = soup[0].attrs
    # Split lemmas and morphs
    lemmas = get_split(attrs, 'lemma')
    morphs = get_split(attrs, 'morph')
    restructured = {
        'identificator': text,
        'lemmas': lemmas,
        'morphs': morphs,
    }
    return Word.construct(**restructured)


def parse_from_xml_str_verse(xml_string: str, children: Sequence[str]) -> Verse:
    """Restructures a single XML <verse> tag into a Verse object."""
    attrs = read_all_xml_tags(xml_string)[0].attrs
    words = [parse_from_xml_str_word(word) for word in children if word]
    restructured = {
        'identificator': attrs['osisID'],
        'words': words,
    }
    return Verse.construct(**restructured)


def parse_from_xml_str_chapter(xml_string: str, children: dict[str, Sequence[str]]) -> Chapter:
    attrs = read_all_xml_tags(xml_string)[0].attrs
    verses = [parse_from_xml_str_verse(a, b) for a, b in children.items()]
    restructured = {
        'identificator': attrs['osisID'],
        'verses': {
            int(v.identificator.split('.')[-1]): v
            for v in verses
        },
    }
    return Chapter.construct(**restructured)


def parse_from_xml_str_book(xml_string: str, children: dict[str, dict[str, Sequence[str]]]) -> Book:
    attrs = read_all_xml_tags(xml_string)[0].attrs
    chapters = [parse_from_xml_str_chapter(a, b) for a, b in children.items()]
    restructured = {
        'identificator': attrs['osisID'],
        'chapters': {
            int(ch.identificator.split('.')[-1]): ch
            for ch in chapters
        },
    }
    return Book.construct(**restructured)


def parse_from_xml_str_bible(children: dict[str, dict[str, dict[str, Sequence[str]]]]) -> Bible:
    books = [parse_from_xml_str_book(a, b) for a, b in children.items()]
    restructured = {
        'identificator': 'BibleKJV',
        'books': {b.identificator: b for b in books},
    }
    return Bible.construct(**restructured)
