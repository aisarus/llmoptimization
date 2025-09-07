import importlib
import inspect
import types
import math

import pytest

def _import_cost():
    # Import efmcalc.cost module and return module object
    mod = importlib.import_module("efmcalc.cost")
    assert isinstance(mod, types.ModuleType)
    return mod

def test_estimate_cost_public_api_exists_and_has_doc():
    cost = _import_cost()
    assert hasattr(cost, "estimate_cost"), "efmcalc.cost should expose estimate_cost"
    fn = cost.estimate_cost
    assert callable(fn), "estimate_cost should be callable"
    # Check it has a docstring to ensure basic documentation quality
    assert inspect.getdoc(fn), "estimate_cost should have a docstring"

@pytest.mark.parametrize(
    "text,model_kw",
    [
        ("Hello world", {}),
        ("", {}),  # empty prompt should not error; tokens likely 0
        ("A"*1000, {}),  # long string handled
        ("Short\nwith\nnewlines", {}),
        ("Emoji 👍🏽 and unicode 測試", {}),
        ("Tab\tseparated\tvalues", {}),
        ("Spaces     and   multiple   spaces", {}),
        ("Punctuation\!?,.;:", {}),
    ],
)
def test_estimate_cost_returns_numeric_token_and_cost(text, model_kw):
    cost = _import_cost()
    result = cost.estimate_cost(text, **model_kw) if model_kw else cost.estimate_cost(text)
    # Accept tuple-like or dict-like returns; enforce presence of count and cost
    if isinstance(result, dict):
        assert "tokens" in result and "cost" in result
        tokens = result["tokens"]
        price = result["cost"]
    elif isinstance(result, (tuple, list)) and len(result) >= 2:
        tokens, price = result[0], result[1]
    else:
        pytest.fail("estimate_cost should return (tokens, cost) or {'tokens','cost'}")

    assert isinstance(tokens, (int, float)) and tokens >= 0
    assert isinstance(price, (int, float)) and price >= 0
    # Increasing text length should generally not reduce tokens
    longer_result = cost.estimate_cost(text + " extra", **model_kw) if model_kw else cost.estimate_cost(text + " extra")
    if isinstance(longer_result, dict):
        more_tokens = longer_result["tokens"]
    else:
        more_tokens = longer_result[0]
    assert more_tokens >= tokens

def test_estimate_cost_handles_non_string_inputs_gracefully():
    cost = _import_cost()
    # Common unexpected types; function should either coerce or raise ValueError/TypeError cleanly
    bad_inputs = [None, 123, 12.34, ["list", "of", "tokens"], {"a": 1}, b"bytes"]
    for inp in bad_inputs:
        try:
            result = cost.estimate_cost(inp)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        # If it doesn't raise, ensure it returns a valid shape
        if isinstance(result, dict):
            assert "tokens" in result and "cost" in result
            assert result["tokens"] >= 0 and result["cost"] >= 0
        elif isinstance(result, (tuple, list)) and len(result) >= 2:
            assert result[0] >= 0 and result[1] >= 0
        else:
            pytest.fail("Unexpected return shape for non-string input")

def test_estimate_cost_is_monotonic_over_multipliers():
    cost = _import_cost()
    base = "token " * 5
    t1 = cost.estimate_cost(base)
    t2 = cost.estimate_cost(base * 2)
    t3 = cost.estimate_cost(base * 4)
    def _tok(x):
        return x["tokens"] if isinstance(x, dict) else x[0]
    assert _tok(t2) >= _tok(t1)
    assert _tok(t3) >= _tok(t2)