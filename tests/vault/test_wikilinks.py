"""TDD tests for the wikilink slug + link helpers (tasks 5.010-5.011)."""

from archlens.vault.wikilinks import disambiguate, render_link, slugify


def test_slugify_handles_spaces_dots_and_case():
    assert slugify("Checkout Service.py") == "checkout-service-py"
    assert slugify("PRD_payments") == "prd-payments"


def test_render_link_wraps_slug():
    assert render_link("Payments") == "[[payments]]"


def test_disambiguate_resolves_case_collisions():
    assert slugify("Foo") == slugify("foo")
    assert disambiguate("foo", set()) == "foo"
    assert disambiguate("foo", {"foo"}) == "foo-2"
    assert disambiguate("foo", {"foo", "foo-2"}) == "foo-3"
