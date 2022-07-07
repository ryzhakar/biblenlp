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

    @abstractmethod
    def as_dict(self):
        pass
    
    @abstractmethod
    def list_children(self) -> Sequence:
        pass


class Word(Corpus):
    """A unit of text."""

    lemmas: Optional[Sequence[str]] = list()
    morphs: Optional[Sequence[str]] = list()

    def get_lemmas(self):
        return self.lemmas

    def get_morphs(self):
        return self.morphs
    
    def get_refers(self):
        pass

    def get_string(self):
        return self.id

    def as_dict(self) -> dict:
        return {
            self.id: {"lemmas": self.lemmas, "morphs": self.morphs}
            }

    def list_children(self) -> Sequence:
        return list()

class Verse(Corpus):
    """An indexed collection of words."""
    
    words: Sequence[Word]
    references: Optional[Sequence[str]] = list()

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.words]

    def get_morphs(self):
        return [x.get_morphs() for x in self.words]

    def get_refers(self):
        return self.references

    def get_string(self):
        return ' '.join([x.get_string() for x in self.words])

    def as_dict(self) -> dict:
        return {x.id: x for x in self.words}

    def list_children(self) -> Sequence:
        return [x.id for x in self.words]

class Chapter(Corpus):
    """A collection of verses."""

    verses: Sequence[Verse]

    def get_lemmas(self):
        return [verse.get_lemmas() for verse in self.verses]

    def get_morphs(self):
        return [x.get_morphs() for x in self.verses]

    def get_refers(self):
        return [x.get_refers() for x in self.verses]

    def get_string(self):
        return ' '.join([x.get_string() for x in self.verses])

    def as_dict(self) -> dict:
        return {x.id: x for x in self.verses}

    def list_children(self) -> Sequence:
        return [x.id for x in self.verses]

class Book(Corpus):
    """A collection of chapters."""

    chapters: Sequence[Chapter]

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.chapters]

    def get_morphs(self):
        return [x.get_morphs() for x in self.chapters]

    def get_refers(self):
        return [x.get_refers() for x in self.chapters]

    def get_string(self):
        return ' '.join([chapter.get_string() for chapter in self.chapters])

    def as_dict(self) -> dict:
        return {x.id: x for x in self.chapters}

    def list_children(self) -> Sequence:
        return [x.id for x in self.chapters]

class Bible(Corpus):
    """A collection of books."""

    books: Sequence[Book]

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.books]

    def get_morphs(self):
        return [x.get_morphs() for x in self.books]

    def get_refers(self):
        return [x.get_refers() for x in self.books]

    def get_string(self):
        return ' '.join([book.get_string() for book in self.books])
    
    def as_dict(self) -> dict:
        return {x.id: x for x in self.books}

    def list_children(self) -> Sequence:
        return [x.id for x in self.books]

    def select_corpus(self, reference: str):
        corpus = self
        ref_split = reference.split('.')
        length = len(ref_split)
        for index in range(length):
            ind = index - length + 1
            if ind == 0:
                local_reference = ref_split
            else:
                local_reference = ref_split[:ind]
            local_reference = '.'.join(local_reference)
            corpus = corpus.as_dict()[local_reference]  # type: ignore
        
        return corpus

