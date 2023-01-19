import itertools
from abc import ABC
from abc import abstractmethod
from collections import Counter
from collections.abc import Iterator

from pydantic import BaseModel

from biblenlp.vectorization.counters import add_the
from biblenlp.vectorization.unique import merge_the


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
