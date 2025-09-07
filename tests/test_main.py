# ruff: noqa: S101
# Tests for CLI main() in the token & cost estimator
# Testing framework: pytest
# These tests focus on argument parsing, interactions with estimate_cost/split_into_chunks,
# and printed output. External functions are mocked.

import builtins
import importlib
import sys
from types import SimpleNamespace
import pytest

# Utility to import the CLI module fresh each time so mocks/argv apply deterministically.
def import_cli_module(module_hint=None):
    """
    Try to import the CLI module containing main(). We first try package-style imports that
    match the code snippet (relative imports .cost/.text_stats imply a package).
    Order of attempts (stop at first that works):
      - efmcalc.main
      - efmcalc.cli
      - main
      - cli
    """
    candidates = module_hint or ["efmcalc.main", "efmcalc.cli", "main", "cli"]
    last_exc = None
    for name in candidates:
        try:
            if name in sys.modules:
                del sys.modules[name]
            return importlib.import_module(name)
        except ImportError as e:
            last_exc = e
    raise last_exc or ImportError("Could not locate CLI module containing main().")

class Argv:
    def __init__(self, *args):
        self.args = ["efmcalc", *args]
    def apply(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", self.args, raising=True)

def patch_cost_and_stats(cli_mod, monkeypatch, estimate_cost_ret=(123, 4.56), chunks=None):
    """
    Patch estimate_cost and split_into_chunks in the CLI module's import context.
    Returns captures of call arguments via SimpleNamespace.
    """
    calls = SimpleNamespace(estimate_cost=[], split_into_chunks=[])
    def fake_estimate_cost(prompt, resp_tokens, pricing):
        calls.estimate_cost.append((prompt, resp_tokens, pricing))
        return estimate_cost_ret
    def fake_split_into_chunks(prompt, chunk_size):
        calls.split_into_chunks.append((prompt, chunk_size))
        return list(chunks or [])
    # Access objects imported by relative path within the cli module
    # They are referenced as cli_mod.estimate_cost and cli_mod.split_into_chunks due to "from .x import ..."
    monkeypatch.setattr(cli_mod, "estimate_cost", fake_estimate_cost, raising=True)
    monkeypatch.setattr(cli_mod, "split_into_chunks", fake_split_into_chunks, raising=True)
    return calls

def read_stdout(capsys):
    out, err = capsys.readouterr()
    return out.strip().splitlines(), err

def test_requires_prompt_arg(monkeypatch, capsys):
    Argv().apply(monkeypatch)
    cli = import_cli_module()
    with pytest.raises(SystemExit):
        cli.main()
    out, err = capsys.readouterr()
    # argparse writes usage/help to stderr on error
    assert "usage:" in err.lower()
    assert "--prompt" in err

def test_happy_path_no_chunk_defaults(monkeypatch, capsys):
    Argv("--prompt", "Hello world").apply(monkeypatch)
    cli = import_cli_module()
    calls = patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(42, 0.21))
    cli.main()
    lines, err = read_stdout(capsys)
    assert any(line.startswith("tokens_total=42 price_usd=0.21") for line in lines)
    # Verify estimate_cost called with defaults resp=0, in1k=0.5, out1k=1.5
    assert len(calls.estimate_cost) == 1
    prompt, resp, pricing = calls.estimate_cost[0]
    assert prompt == "Hello world"
    assert resp == 0
    assert hasattr(pricing, "in1k") and hasattr(pricing, "out1k")
    assert pytest.approx(pricing.in1k, rel=1e-6) == 0.5
    assert pytest.approx(pricing.out1k, rel=1e-6) == 1.5
    # No chunking when chunk=0 default
    assert calls.split_into_chunks == []

def test_with_chunking_prints_chunks(monkeypatch, capsys):
    Argv("--prompt", "ABCDEFG", "--chunk", "3").apply(monkeypatch)
    cli = import_cli_module()
    chunk_list = ["ABC", "DEF", "G"]
    calls = patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(7, 0.003), chunks=chunk_list)
    cli.main()
    lines, err = read_stdout(capsys)
    assert any(line.startswith("tokens_total=7 price_usd=0.003") for line in lines)
    # Chunks printed as specified format
    assert "[chunk 1] ABC" in lines
    assert "[chunk 2] DEF" in lines
    assert "[chunk 3] G" in lines
    # Verify split_into_chunks was called properly
    assert len(calls.split_into_chunks) == 1
    prompt, chunk_size = calls.split_into_chunks[0]
    assert prompt == "ABCDEFG"
    assert chunk_size == 3

def test_custom_resp_and_pricing(monkeypatch, capsys):
    Argv("--prompt", "X", "--resp", "250", "--in1k", "0.9", "--out1k", "2.1").apply(monkeypatch)
    cli = import_cli_module()
    calls = patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(260, 0.987654))
    cli.main()
    lines, err = read_stdout(capsys)
    assert any(line.startswith("tokens_total=260 price_usd=0.987654") for line in lines)
    assert len(calls.estimate_cost) == 1
    prompt, resp, pricing = calls.estimate_cost[0]
    assert prompt == "X"
    assert resp == 250
    assert pytest.approx(pricing.in1k, rel=1e-6) == 0.9
    assert pytest.approx(pricing.out1k, rel=1e-6) == 2.1

@pytest.mark.parametrize("bad_resp", ["NaN", "abc", "-999999999999999999999"])  # parser should error on non-int; huge negative still parses but allowed
def test_invalid_resp_types_raise(monkeypatch, capsys, bad_resp):
    Argv("--prompt", "X", "--resp", bad_resp).apply(monkeypatch)
    cli = import_cli_module()
    # argparse type=int will SystemExit for non-int
    with pytest.raises(SystemExit):
        cli.main()
    out, err = capsys.readouterr()
    assert "invalid int value" in (out + err).lower() or "argument --resp" in (out + err).lower()

@pytest.mark.parametrize("chunk_value, expect_chunks_called", [("0", False), ("-1", False), ("1", True)])
def test_zero_or_negative_chunk_disables_chunking(monkeypatch, capsys, chunk_value, expect_chunks_called):
    Argv("--prompt", "data", "--chunk", chunk_value).apply(monkeypatch)
    cli = import_cli_module()
    calls = patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(4, 0.001), chunks=["d","a","t","a"])
    cli.main()
    lines, err = read_stdout(capsys)
    if expect_chunks_called:
        assert any(line.startswith("[chunk ") for line in lines)
        assert len(calls.split_into_chunks) == 1
    else:
        assert not any(line.startswith("[chunk ") for line in lines)
        assert calls.split_into_chunks == []

def test_very_long_prompt(monkeypatch, capsys):
    long_prompt = "A" * 10000
    Argv("--prompt", long_prompt).apply(monkeypatch)
    cli = import_cli_module()
    calls = patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(10000, 5.0))
    cli.main()
    lines, err = read_stdout(capsys)
    assert any(line.startswith("tokens_total=10000 price_usd=5.0") for line in lines)
    # Ensure prompt passed through unaltered
    assert calls.estimate_cost[0][0] == long_prompt

def test_non_ascii_prompt(monkeypatch, capsys):
    prompt = "こんにちは、世界🌏 — café"
    Argv("--prompt", prompt, "--chunk", "5").apply(monkeypatch)
    cli = import_cli_module()
    chunks = ["こんにちは", "、世界", "🌏 —", " café"]
    patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(9, 0.123), chunks=chunks)
    cli.main()
    lines, err = read_stdout(capsys)
    assert any(line.startswith("tokens_total=9 price_usd=0.123") for line in lines)
    for i, c in enumerate(chunks, 1):
        assert f"[chunk {i}] {c}" in lines

def test_price_format_is_raw_float(monkeypatch, capsys):
    # Ensure price is printed as returned (no extra currency symbols beyond label)
    Argv("--prompt", "X").apply(monkeypatch)
    cli = import_cli_module()
    patch_cost_and_stats(cli, monkeypatch, estimate_cost_ret=(1, 0.5))
    cli.main()
    lines, err = read_stdout(capsys)
    # Should be exactly 'price_usd=<value>'
    matched = [line for line in lines if line.startswith("tokens_total=1 price_usd=")]
    assert matched, "Expected summary line with price_usd"
    # No extra $ sign
    assert "$" not in matched[0]