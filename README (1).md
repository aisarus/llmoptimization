# Philosopher Stone · Minimal Reviewable Project

Small Python lib + CLI to estimate token counts and rough cost for LLM prompts. Includes tests.

## Install & test
```bash
python -m venv .venv && . .venv/bin/activate
pip install -e .[dev]
pytest -q
```

## CLI
```bash
python -m efmcalc --prompt "hello world" --resp 120 --chunk 3
```
