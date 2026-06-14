"""Put the loop_target package root on sys.path so the flat modules import cleanly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
