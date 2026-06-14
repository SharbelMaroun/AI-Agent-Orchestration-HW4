"""Smoke test that the Phase 9 conftest fixtures resolve (task 9.007)."""


def test_fake_clock_fixture(fake_clock):
    assert fake_clock.now() == 0.0
    fake_clock.advance(5)
    assert fake_clock.now() == 5.0


def test_rate_config_factory_fixture(rate_config_factory):
    path = rate_config_factory()
    assert path.is_file()


def test_mock_anthropic_fixture(mock_anthropic):
    client = mock_anthropic(in_tokens=12, out_tokens=7)
    response = client.create(model="claude-opus-4-8", messages=[])
    assert response.usage.input_tokens == 12
    assert response.usage.output_tokens == 7
