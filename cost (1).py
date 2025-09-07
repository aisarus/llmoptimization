from dataclasses import dataclass
from typing import Tuple
from .text_stats import count_tokens

@dataclass(frozen=True)
class Pricing:
    """Simple pricing in USD per 1K tokens."""
    input_per_1k: float = 0.5
    output_per_1k: float = 1.5

def estimate_cost(prompt: str, response_tokens: int, pricing: Pricing = Pricing()) -> Tuple[int, float]:
    """
    Estimate token usage and USD cost for a prompt/response pair.
    
    Calculates input tokens using a whitespace-based token counter, clamps the provided
    response token count to a non-negative integer, then computes total tokens and
    cost using per-1k-token rates from `pricing`. The returned price is rounded to
    6 decimal places.
    
    Parameters:
        prompt: Full input text (e.g., system + user messages); token count is derived
            by a naive whitespace split.
        response_tokens: Expected number of output tokens; will be converted to an
            int and clamped to zero if negative.
        pricing: Per-1k USD rates for input and output tokens (uses `Pricing`
            defaults if not provided).
    
    Returns:
        tuple[int, float]: (total_tokens, total_price_usd)
    """
    input_tokens = count_tokens(prompt)
    out_tokens = max(0, int(response_tokens))
    total_tokens = input_tokens + out_tokens
    price = (input_tokens / 1000.0) * pricing.input_per_1k + (out_tokens / 1000.0) * pricing.output_per_1k
    return total_tokens, round(price, 6)
