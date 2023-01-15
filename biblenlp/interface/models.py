import itertools
from collections import Counter
from collections.abc import Iterator
from functools import reduce

from biblenlp.interface.abstract import CorpusABC


class Word(CorpusABC):
    """A unit of text."""

    lemmas: list[str]
    morphs: list[str]

    def get_lemmas(self) -> Iterator[str]:
        return iter(self.lemmas)

    def get_morphs(self) -> Iterator[str]:
        return iter(self.morphs)

    def get_refers(self) -> Iterator[str]:
        return iter(())

    def get_string(self):
        return self.identificator

    def list_children(self) -> list:
        return list()
    
    @property
    def counter(self) -> Counter[str]:
        return Counter(self.get_lemmas())


class Verse(CorpusABC):
    """An indexed collection of words."""

    words: list[Word]
    references: list[str] = []

    def get_lemmas(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_lemmas()
            for x in self.words
        )

    def get_morphs(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_morphs()
            for x in self.words
        )

    def get_refers(self) -> Iterator[str]:
        return iter(self.references)

    def get_string(self):
        return ' '.join([x.get_string() for x in self.words])

    def list_children(self) -> list:
        return [x.identificator for x in self.words]

    @property
    def counter(self) -> Counter[str]:
        subcounters = [x.counter for x in self.words]
        return reduce(lambda x, y: x + y, subcounters, Counter())


class Chapter(CorpusABC):
    """A mapping of verses."""

    verses: dict[int, Verse]

    def get_lemmas(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            verse.get_lemmas()
            for verse in self.verses.values()
        )

    def get_morphs(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_morphs() for x in self.verses.values()
        )

    def get_refers(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_refers()
            for x in self.verses.values()
        )

    def get_string(self):
        return ' '.join([x.get_string() for x in self.verses.values()])

    def list_children(self) -> list:
        return list(self.verses.keys())

    @property
    def counter(self) -> Counter[str]:
        subcounters = [x.counter for x in self.verses.values()]
        return reduce(lambda x, y: x + y, subcounters, Counter())



class Book(CorpusABC):
    """A collection of chapters."""

    chapters: dict[int, Chapter]

    def get_lemmas(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_lemmas()
            for x in self.chapters.values()
        )

    def get_morphs(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_morphs()
            for x in self.chapters.values()
        )

    def get_refers(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_refers()
            for x in self.chapters.values()
        )

    def get_string(self):
        return ' '.join([chapter.get_string() for chapter in self.chapters.values()])

    def list_children(self) -> list:
        return list(self.chapters.keys())

    @property
    def counter(self) -> Counter[str]:
        subcounters = [x.counter for x in self.chapters.values()]
        return reduce(lambda x, y: x + y, subcounters, Counter())



class Bible(CorpusABC):
    """A collection of books."""

    books: dict[str, Book]

    def get_lemmas(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_lemmas()
            for x in self.books.values()
        )

    def get_morphs(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_morphs() for x in self.books.values()
        )

    def get_refers(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_refers() for x in self.books.values()
        )

    def get_string(self):
        return ' '.join([book.get_string() for book in self.books.values()])

    def list_children(self) -> list:
        return list(self.books.keys())

    @property
    def counter(self) -> Counter[str]:
        subcounters = [x.counter for x in self.books.values()]
        return reduce(lambda x, y: x + y, subcounters, Counter())

    def save(self, filename: str, indent: int = 2):
        """Saves the Bible object to the specified JSON file."""
        with open(filename, 'w') as f:
            f.write(self.json(indent=indent))
