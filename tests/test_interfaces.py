"""TDD tests for the GatekeeperProtocol conformance interface (tasks 8.014-8.015)."""

from archlens.shared.interfaces import GatekeeperProtocol


class _Conforming:
    def call_llm(self, prompt, **kwargs):
        return ""

    def run_subprocess(self, args, **kwargs):
        return None

    def http_get(self, url, **kwargs):
        return None

    def rate_limit_status(self):
        return {}


def test_conforming_class_satisfies_protocol():
    assert isinstance(_Conforming(), GatekeeperProtocol)


def test_missing_method_fails_protocol():
    class Bad:
        def call_llm(self, prompt, **kwargs):
            return ""

    assert not isinstance(Bad(), GatekeeperProtocol)


def test_missing_rate_limit_hook_fails_protocol():
    class NoHook:
        def call_llm(self, prompt, **kwargs):
            return ""

        def run_subprocess(self, args, **kwargs):
            return None

        def http_get(self, url, **kwargs):
            return None

    assert not isinstance(NoHook(), GatekeeperProtocol)
