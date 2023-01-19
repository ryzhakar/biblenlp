from collections.abc import Iterable
from functools import reduce

from utility.decorators import cache_by_key


@cache_by_key
def singularize_the(
    *,
    elements: Iterable[str],
    with_key: str,
) -> set[str]:
    """Makes a set of the elements and saves it for reuse."""
    return set(elements)


@cache_by_key
def merge_the(
    *,
    sets: Iterable[set[str]],
    with_key: str,
) -> set[str]:
    """Combines the sets and saves them for reuse."""
    manually_computed_set: set[str] = reduce(
        lambda x, y: x | y,
        sets,
        set(),
    )
    return manually_computed_set
