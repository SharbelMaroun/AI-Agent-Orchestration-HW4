"""Orchestration runner: SqliteSaver checkpointing and resume (tasks 10.031-10.032)."""

import sqlite3
import weakref
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from ..agents.graph_builder import build_orchestration_graph
from ..shared.config import load_setup


def make_checkpointer(db_path: str | None = None) -> SqliteSaver:
    """Build a SqliteSaver from the configured checkpoint database path (no hardcoded path).

    The sqlite connection is closed automatically when the saver is finalized, so callers never
    leak a database handle (avoids ResourceWarning: unclosed database on garbage collection).
    """
    db_path = db_path or load_setup().sdk.checkpoint_db
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    saver = SqliteSaver(conn)
    weakref.finalize(saver, conn.close)
    return saver


def make_runner(sdk, db_path: str | None = None, interrupt_after=None):
    """Compile the orchestration graph with a SqliteSaver checkpointer for resumable runs."""
    return build_orchestration_graph(
        sdk, checkpointer=make_checkpointer(db_path), interrupt_after=interrupt_after)


def resume_run(graph, thread_id: str):
    """Restore the latest checkpoint for ``thread_id`` and continue from the next pending node."""
    return graph.invoke(None, {"configurable": {"thread_id": thread_id}})
