from collections import Counter
from collections.abc import Iterable
from functools import reduce

from biblenlp.utility.decorators import cache_by_key


def count_the(*, elements: Iterable[str]) -> Counter[str]:
    """Counts the number of times each element appears in the tuple."""
    return Counter(elements)


@cache_by_key
def add_the(
    *,
    counters: Iterable[Counter[str]],
    with_key: str,
) -> Counter[str]:
    """Combines the counts and saves them for reuse."""
    manually_computed_counter: Counter[str] = reduce(
        lambda x, y: x + y,
        counters,
        Counter(),
    )
    return manually_computed_counter
