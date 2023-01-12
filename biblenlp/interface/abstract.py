from collections.abc import Iterator
from abc import ABC, abstractmethod
from pydantic import BaseModel


class CorpusABC(BaseModel, ABC):
    """A corpus is a collection of words."""

    identificator: str

    def __hash__(self):
        return hash(self.identificator)

    @abstractmethod
    def get_lemmas(self) -> Iterator[str]:
        pass

    @abstractmethod
    def get_refers(self) -> Iterator[str]:
        pass

    @abstractmethod
    def get_morphs(self) -> Iterator[str]:
        pass

    @abstractmethod
    def get_string(self):
        pass

    @abstractmethod
    def list_children(self):
        pass


