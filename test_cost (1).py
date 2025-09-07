from pytest import approx
from efmcalc.cost import estimate_cost, Pricing

def test_estimate_cost_basic():
    total_tokens, price = estimate_cost("hello world", 100, Pricing(1.0, 2.0))
    assert total_tokens == 102
    assert price == approx(0.202, rel=1e-9)

def test_estimate_cost_nonnegative():
    total_tokens, price = estimate_cost("x", -50)
    assert total_tokens == 1
    assert price >= 0.0
