# Philosophe r Stone · Minimal Reviewable Project

Short CLI + lib to estimate token counts and cost for LLM prompts.

## Features
- `efmcalc.cost.estimate_cost` — rough token & price estimator.
- `efmcalc.text_stats.split_into_chunks` — naive chunking helper.
- CLI: `python -m efmcalc --help`

## Install & test
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .
pytest -q
```

## Why this repo
Designed to provoke AI code review (CodeRabbit): small, readable, tests, docstrings.
