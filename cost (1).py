from dataclasses import dataclass
from typing import Tuple
from .text_stats import count_tokens

@dataclass(frozen=True)
class Pricing:
    """Simple pricing in USD per 1K tokens."""
    input_per_1k: float = 0.5
    output_per_1k: float = 1.5

def estimate_cost(prompt: str, response_tokens: int, pricing: Pricing = Pricing()) -> Tuple[int, float]:
    """Estimate token usage and price.

    Args:
        prompt: input text (user + system).
        response_tokens: expected output tokens from the model.
        pricing: per-1k pricing (input/output).

    Returns:
        total_tokens: int
        total_price_usd: float

    Notes:
        - Token counter is naive (whitespace split). Suitable for ballpark figures only.
    """
    input_tokens = count_tokens(prompt)
    out_tokens = max(0, int(response_tokens))
    total_tokens = input_tokens + out_tokens
    price = (input_tokens / 1000.0) * pricing.input_per_1k + (out_tokens / 1000.0) * pricing.output_per_1k
    return total_tokens, round(price, 6)
