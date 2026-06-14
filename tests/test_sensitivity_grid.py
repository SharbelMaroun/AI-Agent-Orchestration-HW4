"""TDD tests for OAT sensitivity variant generation (task 15.003)."""

from archlens.metrics.sensitivity_grid import PARAMS, oat_variants
from archlens.shared.config import load_setup


def _block():
    return load_setup().sensitivity


def test_variants_cover_all_four_parameters():
    variants = oat_variants(_block())
    assert set(variants) == set(PARAMS)


def test_one_factor_varied_others_at_baseline():
    block = _block()
    variants = oat_variants(block)
    for param, rows in variants.items():
        assert len(rows) == len(getattr(block, param))
        for row in rows:
            for other in PARAMS:
                if other != param:
                    assert row[other] == block.baseline[other]


def test_varied_factor_matches_its_range():
    block = _block()
    variants = oat_variants(block)
    for param, rows in variants.items():
        assert [row[param] for row in rows] == list(getattr(block, param))
