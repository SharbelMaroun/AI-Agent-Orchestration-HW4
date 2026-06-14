"""Core service every feature imports — a planted single point of failure (SPOF)."""


def serve(payload):
    """The one entry point all features route through."""
    return {"ok": True, "payload": payload}
