from collections import Counter
from functools import lru_cache
from functools import reduce


CACHE_REGISTRY: dict[str, Counter[str]] = {}


@lru_cache
def count_the(*, elements: tuple[str, ...]) -> Counter[str]:
    """Counts the number of times each element appears in the tuple."""
    return Counter(elements)


def add_the(
    *,
    counters: list[Counter[str]],
    with_key: str,
) -> Counter[str]:
    """Combines the counts and saves them for reuse."""
    potentially_cached = CACHE_REGISTRY.get(with_key)
    if potentially_cached is not None:
        return potentially_cached
    manually_computed_counter: Counter[str] = reduce(
        lambda x, y: x + y,
        counters,
        Counter(),
    )
    CACHE_REGISTRY[with_key] = manually_computed_counter
    return manually_computed_counter
