"""Interactive repo picker for the ``start`` flow — list the suggestions, accept a number or a URL.

I/O is injected (``input_fn``/``output_fn``) so the flow is unit-testable and never blocks the suite.
"""

_URL_PREFIXES = ("http://", "https://", "git@")


def resolve_choice(raw: str, suggested) -> str | None:
    """Map a raw answer to a clone URL: a pasted git URL, or a 1-based index into ``suggested``."""
    raw = raw.strip()
    if raw.startswith(_URL_PREFIXES):
        return raw
    if raw.isdigit() and 1 <= int(raw) <= len(suggested):
        return suggested[int(raw) - 1].url
    return None


def pick_repo(suggested, input_fn=input, output_fn=print) -> str | None:
    """Show the suggested repos, read one answer, and return the chosen URL (or None if invalid)."""
    output_fn("Which repository should I clone? Pick a number, or paste a git URL:")
    for index, repo in enumerate(suggested, start=1):
        note = f"  - {repo.note}" if repo.note else ""
        output_fn(f"  {index}) {repo.name:10} {repo.url}{note}")
    return resolve_choice(input_fn("> "), suggested)
