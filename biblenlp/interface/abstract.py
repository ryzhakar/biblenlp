from __future__ import annotations
import itertools
import math
from abc import ABC
from abc import abstractmethod
from collections import Counter
from collections.abc import Iterator

from pydantic import BaseModel
from immutables import Map

from biblenlp.vectorization.counters import add_the
from biblenlp.vectorization.unique import merge_the
from biblenlp.vectorization.mappings import combine_the


class VectorizibleABC(ABC):
    @abstractmethod
    def get_lemmas(self) -> Iterator[str]:
        pass

    @abstractmethod
    def get_morphs(self) -> Iterator[str]:
        pass

    @property
    @abstractmethod
    def counter(self) -> Counter[str]:
        pass

    @property
    @abstractmethod
    def unique_lemmas(self) -> set[str]:
        pass

    @property
    @abstractmethod
    def lemma_word_mapping(self) -> Map[str, tuple[VectorizibleABC, ...]]:
        pass

    @abstractmethod
    def tf(self) -> dict[str, float]:
        pass


class CorpusABC(BaseModel, VectorizibleABC):
    """A corpus is a collection of words."""

    identificator: str

    def __hash__(self):
        return hash(self.identificator)

    @property
    @abstractmethod
    def subcorpora(self) -> Iterator[VectorizibleABC]:
        """A dictionary of subcorpora."""

    def get_lemmas(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_lemmas()
            for x in self.subcorpora
        )

    def get_morphs(self) -> Iterator[str]:
        return itertools.chain.from_iterable(
            x.get_morphs()
            for x in self.subcorpora
        )

    @property
    def counter(self) -> Counter[str]:
        subcounters = (x.counter for x in self.subcorpora)
        return add_the(counters=subcounters, with_key=self.identificator)

    @property
    def unique_lemmas(self) -> set[str]:
        return merge_the(
            sets=(x.unique_lemmas for x in self.subcorpora),
            with_key=self.identificator,
        )

    @property
    def lemma_word_mapping(self) -> Map[str, tuple[VectorizibleABC, ...]]:
        """A mapping of lemmas to words."""
        return combine_the(
            mappings=(x.lemma_word_mapping for x in self.subcorpora),
            with_key=self.identificator,
        )
        

    def count_occurences_of(self, *, terms: set[str]) -> Counter[str]:
        """How many of the subcorpora contain the terms."""
        term_overlaps = (
            terms.intersection(x.unique_lemmas)
            for x in self.subcorpora
        )
        all_occurrences_in_subcorpora = itertools.chain.from_iterable(
            term_overlaps,
        )
        return Counter(all_occurrences_in_subcorpora)


    def idf(self, terms: set[str]) -> dict[str, float]:
        """Inverse document frequency."""
        occurrences = self.count_occurences_of(terms=terms)
        subcorpora_count = sum(1 for _ in self.subcorpora)
        return {
            term: math.log(subcorpora_count / occurrences[term])
            for term in occurrences
        }

    def tf(self) -> dict[str, float]:
        """Term frequency."""
        return {
            term: count / sum(self.counter.values())
            for term, count in self.counter.items()
        }
