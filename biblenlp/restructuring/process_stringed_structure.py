from bs4 import BeautifulSoup

from biblenlp.interface.models import Bible
from biblenlp.interface.models import Book
from biblenlp.interface.models import Chapter
from biblenlp.interface.models import Verse
from biblenlp.interface.models import Word


def read_all_xml_tags(xml_string: str):
    soup = BeautifulSoup(xml_string, 'xml')
    return list(soup.find_all())


def get_split(dictionary: dict, key: str) -> list[str]:
    """Returns a list of values for a given key in a dictionary."""
    value = dictionary.get(key)
    if value is None:
        return []
    else:
        return value.split(' ')


def parse_from_xml_str_word(xml_string: str) -> Word:
    """Restructures a single XML <w> tag into a Word object."""
    xml_soup = read_all_xml_tags(xml_string)
    text = xml_soup[0].text
    attrs = xml_soup[0].attrs
    lemmas = get_split(attrs, 'lemma')
    morphs = get_split(attrs, 'morph')
    return Word.construct(
        identificator=text,
        lemmas=lemmas,
        morphs=morphs,
    )


RawWordsType = list[str]


def parse_from_xml_str_verse(xml_string: str, xml_words: RawWordsType) -> Verse:
    """Restructures a single XML <verse> tag into a Verse object."""
    attrs = read_all_xml_tags(xml_string)[0].attrs
    words = [parse_from_xml_str_word(word) for word in filter(None, xml_words)]
    return Verse.construct(
        identificator=attrs['osisID'],
        words=words,
    )


RawChapterType = dict[str, RawWordsType]


def parse_from_xml_str_chapter(xml_string: str, xml_verses: RawChapterType) -> Chapter:
    chapter_identificator = read_all_xml_tags(xml_string)[0].attrs['osisID']
    verses = (
        parse_from_xml_str_verse(raw_verse, raw_words)
        for raw_verse, raw_words in xml_verses.items()
    )
    return Chapter.construct(
        identificator=chapter_identificator,
        verses={
            int(verse.identificator.split('.')[-1]): verse
            for verse in verses
        },
    )


RawBookType = dict[str, RawChapterType]


def parse_from_xml_str_book(xml_string: str, xml_chapters: RawBookType) -> Book:
    book_identificator = read_all_xml_tags(xml_string)[0].attrs['osisID']
    chapters = (
        parse_from_xml_str_chapter(a, b)
        for a, b in xml_chapters.items()
    )
    return Book.construct(
        identificator=book_identificator,
        chapters={
            int(ch.identificator.split('.')[-1]): ch
            for ch in chapters
        },
    )


RawBibleType = dict[str, RawBookType]


def parse_from_xml_str_bible(children: RawBibleType) -> Bible:
    books = (
        parse_from_xml_str_book(a, b)
        for a, b in children.items()
    )
    return Bible.construct(
        identificator='BibleKJV',
        books={b.identificator: b for b in books},
    )
