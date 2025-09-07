# ruff: noqa

from efmcalc.cost import estimate_cost, Pricing

def test_estimate_cost_basic():
    total_tokens, price = estimate_cost("hello world", 100, Pricing(1.0, 2.0))
    assert total_tokens == 102
    # 2 input tokens * $1/1k + 100 output * $2/1k = 0.002 + 0.2
    assert abs(price - 0.202) < 1e-9

def test_estimate_cost_nonnegative():
    total_tokens, price = estimate_cost("x", -50)
    assert total_tokens == 1
    assert price >= 0.0

# Framework note: Tests use pytest-style assertions and exceptions.
# If unittest is configured, these pytest-style tests are still valid when run via pytest.

import math
import pytest

def test_estimate_cost_empty_prompt_counts_zero_or_one_tokens_consistently():
    # Depending on implementation, empty prompt may yield 0 tokens (preferred) or 1 (legacy behavior).
    # We assert price correctness for both possibilities while locking total_tokens to be non-negative and small.
    total_tokens, price = estimate_cost("", 0, Pricing(1.0, 2.0))
    assert total_tokens in (0, 1)
    assert price == pytest.approx((total_tokens / 1000.0) * 1.0, rel=0, abs=1e-12)

@pytest.mark.parametrize(
    "prompt,expected_input_tokens",
    [
        ("hello world", 2),
        ("  leading and trailing  ", 3),  # "leading", "and", "trailing"
        ("tabs\tand   spaces", 3),
        ("punctuation, should; not\! create? extra.", 5),
        ("new\nlines\nand\nwords", 4),
        ("emoji 😀 test", 2),
        ("中文 测试", 2),
    ],
)
def test_estimate_cost_tokenization_basics(prompt, expected_input_tokens):
    total_tokens, price = estimate_cost(prompt, 0, Pricing(1.5, 0.0))
    # total_tokens should be input tokens (since output=0)
    assert total_tokens == expected_input_tokens
    assert price == pytest.approx((expected_input_tokens / 1000.0) * 1.5, rel=0, abs=1e-12)

def test_estimate_cost_negative_output_is_clamped_to_zero_or_handled_gracefully():
    total_tokens, price = estimate_cost("x y z", -100, Pricing(1.0, 2.0))
    # Implementation in existing tests expects non-negative price; ensure no exception and sane totals
    assert total_tokens >= 3
    assert price >= 0.0

def test_estimate_cost_large_output_and_custom_pricing_precision():
    prompt = "a b c d e"  # 5 input tokens
    output_tokens = 123456
    pricing = Pricing(input_per_1k=0.12345, output_per_1k=0.54321)
    total_tokens, price = estimate_cost(prompt, output_tokens, pricing)
    assert total_tokens == 5 + output_tokens
    expected_price = (5/1000.0)*pricing.input_per_1k + (output_tokens/1000.0)*pricing.output_per_1k
    assert price == pytest.approx(expected_price, rel=1e-12, abs=1e-12)

def test_estimate_cost_zero_rates_results_in_zero_price():
    total_tokens, price = estimate_cost("one two three", 42, Pricing(0.0, 0.0))
    assert total_tokens == 3 + 42
    assert price == 0.0

def test_pricing_accepts_positional_and_keyword_args_and_is_immutable_like_dataclass():
    # Validate that Pricing works with positional args
    p1 = Pricing(1.0, 2.0)
    assert p1.input_per_1k == 1.0 and p1.output_per_1k == 2.0
    # Validate keyword args
    p2 = Pricing(output_per_1k=0.2, input_per_1k=0.1)
    assert p2.input_per_1k == 0.1 and p2.output_per_1k == 0.2
    # If dataclass(frozen=True), mutation should raise; if not, this block is skipped safely.
    if getattr(p1, "__setattr__", None) is object.__setattr__:
        with pytest.raises(Exception):
            p1.input_per_1k = 9.9

@pytest.mark.parametrize(
    "prompt,output_tokens,pricing,expected",
    [
        ("hello", 0, Pricing(1.0, 2.0), ((1), (1/1000.0)*1.0)),
        ("hello there", 10, Pricing(0.0, 1.0), ((2+10), (10/1000.0)*1.0)),
        ("", 1000, Pricing(1.0, 0.5), (pytest.approx(1000, abs=1e-12), (1000/1000.0)*0.5)),
    ],
)
def test_estimate_cost_various_combinations(prompt, output_tokens, pricing, expected):
    total_tokens, price = estimate_cost(prompt, output_tokens, pricing)
    exp_total, exp_price = expected
    assert total_tokens == exp_total
    assert price == pytest.approx(exp_price, rel=0, abs=1e-12)

def test_estimate_cost_does_not_mutate_inputs():
    prompt = "stay same"
    output_tokens = 7
    pricing = Pricing(0.1, 0.2)
    prompt_before = prompt[:]
    total_before = output_tokens
    _, _ = estimate_cost(prompt, output_tokens, pricing)
    assert prompt == prompt_before
    assert output_tokens == total_before
    assert pricing.input_per_1k == 0.1 and pricing.output_per_1k == 0.2

def test_pricing_rejects_negative_rates_if_validated_otherwise_price_can_be_negative_only_if_rates_negative():
    # If the dataclass validates, we expect an exception; otherwise verify price math remains sane.
    try:
        p = Pricing(-0.1, 0.2)
    except Exception:
        pytest.skip("Pricing validation prohibits negative rates.")
    else:
        total_tokens, price = estimate_cost("x", 10, p)
        expected = (1/1000.0)*(-0.1) + (10/1000.0)*(0.2)
        assert total_tokens == 11
        assert price == pytest.approx(expected, rel=0, abs=1e-12)

def test_estimate_cost_whitespace_only_prompt():
    total_tokens, price = estimate_cost("   \t \n  ", 5, Pricing(1.0, 1.0))
    # Whitespace-only should count as zero tokens
    assert total_tokens == 5
    assert price == pytest.approx((5/1000.0)*1.0, rel=0, abs=1e-12)

def test_estimate_cost_surrogates_and_high_unicode():
    prompt = "Unicode test 🧪"
    total_tokens, _ = estimate_cost(prompt, 0, Pricing(0.1, 0.2))
    # Expect 2 tokens if splitting on whitespace
    assert total_tokens in (1, 2)