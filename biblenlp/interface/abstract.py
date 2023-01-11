from abc import ABC, abstractmethod
from pydantic import BaseModel


class Corpus(BaseModel, ABC):
    """A corpus is a collection of words."""

    identificator: str

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
    def list_children(self):
        pass


