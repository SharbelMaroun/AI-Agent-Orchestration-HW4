"""Wikilink slug + link helpers reused by every page generator (tasks 5.010-5.011)."""

import re

_NON_SLUG = re.compile(r"[^a-z0-9]+")


def slugify(name: str) -> str:
    """Lowercase and collapse runs of non-alphanumerics into single hyphens."""
    slug = _NON_SLUG.sub("-", name.lower()).strip("-")
    return slug or "page"


def disambiguate(slug: str, taken: set[str]) -> str:
    """Append -2, -3, ... so a slug never collides with one already taken."""
    if slug not in taken:
        return slug
    index = 2
    while f"{slug}-{index}" in taken:
        index += 1
    return f"{slug}-{index}"


def render_link(name: str) -> str:
    return f"[[{slugify(name)}]]"
