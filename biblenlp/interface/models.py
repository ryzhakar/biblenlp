from collections import Counter
from collections.abc import Iterator

from pydantic import BaseModel

from biblenlp.interface.abstract import CorpusABC
from biblenlp.interface.abstract import VectorizibleABC
from biblenlp.vectorization.counters import count_the
from biblenlp.vectorization.unique import singularize_the


class Word(BaseModel, VectorizibleABC):
    """A unit of text."""
    identificator: str
    lemmas: list[str]
    morphs: list[str]

    def get_lemmas(self) -> Iterator[str]:
        return iter(self.lemmas)

    def get_morphs(self) -> Iterator[str]:
        return iter(self.morphs)

    @property
    def counter(self) -> Counter[str]:
        immutable_lemmas = self.lemmas
        return count_the(elements=immutable_lemmas)

    @property
    def unique_lemmas(self) -> set[str]:
        return singularize_the(
            elements=self.lemmas,
            with_key=self.identificator,
        )


class Verse(CorpusABC):
    """An indexed collection of words."""
    words: list[Word]
    references: list[str] = []

    @property
    def subcorpora(self) -> Iterator[Word]:
        return iter(self.words)


class Chapter(CorpusABC):
    """A mapping of verses."""
    verses: dict[int, Verse]

    @property
    def subcorpora(self) -> Iterator[Verse]:
        return iter(self.verses.values())


class Book(CorpusABC):
    """A collection of chapters."""
    chapters: dict[int, Chapter]

    @property
    def subcorpora(self) -> Iterator[Chapter]:
        return iter(self.chapters.values())


class Bible(CorpusABC):
    """A collection of books."""

    books: dict[str, Book]

    @property
    def subcorpora(self) -> Iterator[Book]:
        return iter(self.books.values())

    def save(self, filename: str, indent: int = 2):
        """Saves the Bible object to the specified JSON file."""
        with open(filename, 'w') as f:
            f.write(self.json(indent=indent))
