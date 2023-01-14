import functools
import re
from collections.abc import Iterator


def starts_with_opening_tags(line: str, tags: list[str]) -> bool:
    """Returns True if line starts with any of the provided tags."""
    tag_pattern = '|'.join(tags)
    match = re.match(fr'\s*<({tag_pattern})', line)
    return match is not None


def starts_with_blacklisted(line: str) -> bool:
    """Returns True if line starts with a blacklisted tag."""
    blacklist = {
        '<div type="colophon"',
    }
    return any(line.startswith(x) for x in blacklist)


def starts_with_whitelisted(line: str, tags: list[str]) -> bool:
    """Combines starts_with_tags and starts_with_blacklisted."""
    has_a_tag = starts_with_opening_tags(line, tags)
    is_blacklisted = starts_with_blacklisted(line)
    return has_a_tag and not is_blacklisted


def filter_lines(
    *,
    tags: list[str],
    lines: list[str],
    filter_method,
) -> Iterator[str]:
    """Leaves only lines that start with specified tags."""
    stripped_lines = map(str.lstrip, lines)
    return filter(functools.partial(filter_method, tags=tags), stripped_lines)
