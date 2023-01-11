from biblenlp.interface.abstract import Corpus


class Word(Corpus):
    """A unit of text."""

    lemmas: list[str]
    morphs: list[str]

    def get_lemmas(self):
        return self.lemmas

    def get_morphs(self):
        return self.morphs
    
    def get_refers(self):
        pass

    def get_string(self):
        return self.identificator

    def as_dict(self) -> dict:
        return {
            self.identificator: {"lemmas": self.lemmas, "morphs": self.morphs}
            }

    def list_children(self) -> list:
        return list()

class Verse(Corpus):
    """An indexed collection of words."""
    
    words: list[Word] = []
    references: list[str] = []

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.words]

    def get_morphs(self):
        return [x.get_morphs() for x in self.words]

    def get_refers(self):
        return self.references

    def get_string(self):
        return ' '.join([x.get_string() for x in self.words])

    def as_dict(self) -> dict:
        return {x.identificator: x for x in self.words}

    def list_children(self) -> list:
        return [x.identificator for x in self.words]

class Chapter(Corpus):
    """A collection of verses."""

    verses: list[Verse]

    def get_lemmas(self):
        return [verse.get_lemmas() for verse in self.verses]

    def get_morphs(self):
        return [x.get_morphs() for x in self.verses]

    def get_refers(self):
        return [x.get_refers() for x in self.verses]

    def get_string(self):
        return ' '.join([x.get_string() for x in self.verses])

    def as_dict(self) -> dict:
        return {x.identificator: x for x in self.verses}

    def list_children(self) -> list:
        return [x.identificator for x in self.verses]

class Book(Corpus):
    """A collection of chapters."""

    chapters: list[Chapter]

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.chapters]

    def get_morphs(self):
        return [x.get_morphs() for x in self.chapters]

    def get_refers(self):
        return [x.get_refers() for x in self.chapters]

    def get_string(self):
        return ' '.join([chapter.get_string() for chapter in self.chapters])

    def as_dict(self) -> dict:
        return {x.identificator: x for x in self.chapters}

    def list_children(self) -> list:
        return [x.identificator for x in self.chapters]

class Bible(Corpus):
    """A collection of books."""

    books: list[Book]

    def get_lemmas(self):
        return [x.get_lemmas() for x in self.books]

    def get_morphs(self):
        return [x.get_morphs() for x in self.books]

    def get_refers(self):
        return [x.get_refers() for x in self.books]

    def get_string(self):
        return ' '.join([book.get_string() for book in self.books])
    
    def as_dict(self) -> dict:
        return {x.identificator: x for x in self.books}

    def list_children(self) -> list:
        return [x.identificator for x in self.books]

    def select_corpus(self, reference: str):
        corpus = self
        ref_split = reference.split('.')
        length = len(ref_split)
        for index in range(length):
            indA = 0-length
            indB = index + 1
            local_reference = '.'.join(ref_split[indA:indB])
            corpus = corpus.as_dict().get(local_reference)  # type: ignore
        
        return corpus


