# QAAgent Prompt
Version: 1.00
Variables: coverage_min

Run pytest, coverage (>= {coverage_min}), and ruff through the SDK; record tests-green,
coverage percentage, and ruff violation count into stop_eval.
