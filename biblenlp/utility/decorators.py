from collections.abc import Callable
from collections.abc import Iterable
from functools import wraps
from typing import TypeVar


SomeData = TypeVar('SomeData')
Processor = Callable[..., SomeData]


def cache_by_key(processor: Processor) -> Processor:
    """Caches the result of a function by its key."""

    @wraps(processor)
    def wrapper(*, with_key: str, **kwargs: Iterable[SomeData]) -> SomeData:
        cache: dict[str, SomeData] = {}
        if with_key in cache:
            return cache[with_key]
        result = processor(with_key=with_key, **kwargs)
        cache[with_key] = result
        return result

    return wrapper
