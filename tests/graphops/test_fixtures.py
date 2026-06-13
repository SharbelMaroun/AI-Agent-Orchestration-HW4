"""Smoke tests for the synthetic graph fixtures (task 6.005)."""

from fixtures import (
    build_auth_path,
    build_barbell,
    build_chain,
    build_composite,
    build_star,
    build_two_community,
)

from archlens.graphops.loader import load_graph


def _counts(graph_dict: dict) -> tuple[int, int]:
    loaded = load_graph(graph_dict)
    return loaded.number_of_nodes(), loaded.number_of_edges()


def test_star_counts():
    assert _counts(build_star(5)) == (5, 4)


def test_chain_counts():
    assert _counts(build_chain(4)) == (4, 3)


def test_barbell_counts():
    assert _counts(build_barbell(3)) == (6, 7)


def test_two_community_counts():
    assert _counts(build_two_community()) == (6, 7)


def test_auth_path_counts():
    assert _counts(build_auth_path()) == (4, 3)


def test_composite_counts():
    assert _counts(build_composite()) == (9, 8)


def test_every_fixture_loads_without_schema_error():
    for builder in (
        build_star,
        build_chain,
        build_barbell,
        build_two_community,
        build_auth_path,
        build_composite,
    ):
        loaded = load_graph(builder())
        assert loaded.number_of_nodes() >= 1
