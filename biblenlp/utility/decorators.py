from collections.abc import Callable
from collections.abc import Iterable
from functools import wraps
from typing import TypeVar


SomeData = TypeVar('SomeData')
Processor = Callable[..., SomeData]
CACHE: dict[Callable, dict] = {}


def cache_by_key(processor: Processor) -> Processor:
    """Caches the result of a function by its key."""
    global CACHE

    @wraps(processor)
    def wrapper(*, with_key: str, **kwargs: Iterable[SomeData]) -> SomeData:
        CACHE[processor] = CACHE.get(processor, {})
        cache: dict[str, SomeData] = CACHE[processor]
        if with_key in cache:
            return cache[with_key]
        result = processor(with_key=with_key, **kwargs)
        cache[with_key] = result
        return result

    return wrapper
