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
