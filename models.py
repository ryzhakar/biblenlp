from abc import ABC, abstractmethod
from typing import Optional, Sequence
from pydantic import BaseModel




class Corpus(BaseModel, ABC):
    """A corpus is a collection of words."""

    id: str

    @abstractmethod
    def get_lemmas(self):
        pass

    @abstractmethod
    def get_refers(self):
        pass

    @abstractmethod
    def get_morphs(self):
        pass

    @abstractmethod
    def get_string(self):
        pass


class Word(Corpus):
    """A unit of text."""

    source: str
    lemmas: Optional[Sequence[str]] = list()
    morphs: Optional[Sequence[str]] = list()

    def get_lemmas(self):
        return self.lemmas

    def get_morphs(self):
        return self.morphs
    
    def get_refers(self):
        pass

    def get_string(self):
        return self.source


class Verse(Corpus):
    """An indexed collection of words."""
    
    words: Sequence[Word]
    references: Optional[Sequence[str]] = list()

    def get_lemmas(self):
        return [word.get_lemmas() for word in self.words]

    def get_morphs(self):
        return [word.get_morphs() for word in self.words]

    def get_refers(self):
        return self.references

    def get_string(self):
        return ' '.join([word.get_string() for word in self.words])


class Chapter(Corpus):
    """A collection of verses."""

    verses: Sequence[Verse]

    def get_lemmas(self):
        return [verse.get_lemmas() for verse in self.verses]

    def get_morphs(self):
        return [verse.get_morphs() for verse in self.verses]

    def get_refers(self):
        return [verse.get_refers() for verse in self.verses]

    def get_string(self):
        return ' '.join([verse.get_string() for verse in self.verses])

class Book(Corpus):
    """A collection of chapters."""

    chapters: Sequence[Chapter]

    def get_lemmas(self):
        return [chapter.get_lemmas() for chapter in self.chapters]

    def get_morphs(self):
        return [chapter.get_morphs() for chapter in self.chapters]

    def get_refers(self):
        return [chapter.get_refers() for chapter in self.chapters]

    def get_string(self):
        return ' '.join([chapter.get_string() for chapter in self.chapters])