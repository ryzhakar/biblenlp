import itertools
from collections.abc import Iterable
from functools import reduce
from typing import TypeVar

from immutables import Map

from biblenlp.utility.decorators import cache_by_key

GenericElement = TypeVar('GenericElement')


LemmaToWordsMapping = Map[str, tuple[GenericElement, ...]]


def merge_two_mappings(
    bigger_mapping: LemmaToWordsMapping,
    smaller_mapping: LemmaToWordsMapping,
) -> LemmaToWordsMapping:
    all_keys = set(bigger_mapping.keys()) | set(smaller_mapping.keys())
    items = iter(
        (
            key, tuple(
                set(
                    itertools.chain(
                        bigger_mapping.get(key, ()),
                        smaller_mapping.get(key, ()),
                    ),
                ),
            ),
        ) for key in all_keys
    )
    return Map(items)


@cache_by_key
def combine_the(
    *,
    mappings: Iterable[LemmaToWordsMapping],
    with_key: str,
) -> LemmaToWordsMapping:
    """Combines the mappings and saves them for reuse."""
    manually_computed_mapping: LemmaToWordsMapping = reduce(
        merge_two_mappings,
        mappings,
        Map(),
    )
    return manually_computed_mapping
