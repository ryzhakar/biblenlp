from textwrap import indent
from typing import Sequence
from bs4 import BeautifulSoup
from .models import Bible, Book, Chapter, Verse, Word

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

def restructure_soup_word(xml_string: str) -> Word:
    """Restructures a single XML <w> tag into a Word object."""
    soup = read_all_xml_tags(xml_string)
    text = soup[0].text
    attrs = soup[0].attrs
    # Split lemmas and morphs
    lemmas = get_split(attrs,'lemma')
    morphs = get_split(attrs,'morph')
    restructured = {
            'id': text,
            'lemmas': lemmas,
            'morphs': morphs,
        }
    return Word(**restructured)

def restructure_soup_verse(xml_string: str, children: Sequence[str]) -> Verse:
    """Restructures a single XML <verse> tag into a Verse object."""
    attrs = read_all_xml_tags(xml_string)[0].attrs
    words = [restructure_soup_word(word) for word in children if word]
    restructured = {
            'id': attrs['osisID'],
            'words': words,
        }
    return Verse(**restructured)

def restructure_soup_chapter(xml_string: str, children: dict[str, Sequence[str]]) -> Chapter:
    attrs = read_all_xml_tags(xml_string)[0].attrs
    verses = [restructure_soup_verse(a, b) for a, b in children.items()]
    restructured = {
            'id': attrs['osisID'],
            'verses': verses,
        }
    return Chapter(**restructured)

def restructure_soup_book(xml_string: str, children: dict[str, dict[str, Sequence[str]]]) -> Book:
    attrs = read_all_xml_tags(xml_string)[0].attrs
    chapters = [restructure_soup_chapter(a, b) for a, b in children.items()]
    restructured = {
            'id': attrs['osisID'],
            'chapters': chapters,
        }
    return Book(**restructured)

def restructure_soup_bible(children: dict[str, dict[str, dict[str, Sequence[str]]]]) -> Bible:
    books = [restructure_soup_book(a, b) for a, b in children.items()]
    restructured = {
            'id': 'BibleKJV',
            'books': books,
        }
    return Bible(**restructured)


if __name__ == "__main__":
    original = input("Path to the original XML: ")
    filename = input("Path for the new file: ")
    from untangle_xml import untangle_osis
    bible = untangle_osis(original)
    pybible = restructure_soup_bible(bible) # type: ignore

    with open(filename, 'w+') as f:
        j = pybible.json(indent=0)
        f.write(j)