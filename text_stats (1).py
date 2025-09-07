from __future__ import annotations
from typing import List

def count_tokens(text: str) -> int:
    """Ultra-naive token counter: split by whitespace."""
    if not text:
        return 0
    return len(text.split())

def split_into_chunks(text: str, max_tokens: int) -> list[str]:
    """
    Split text into whitespace-delimited chunks, each containing at most `max_tokens` tokens.
    
    This function tokenizes `text` using str.split() (whitespace) and groups tokens into consecutive chunks no larger than `max_tokens`.
    Empty or all-whitespace input returns an empty list. Tokens are rejoined with single spaces in each returned chunk.
    
    Args:
        text: Source string to split.
        max_tokens: Positive integer limit for tokens per chunk.
    
    Returns:
        A list of chunk strings, each containing up to `max_tokens` tokens.
    
    Raises:
        ValueError: If `max_tokens` is not a positive integer.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    cur: list[str] = []
    for w in words:
        if len(cur) + 1 > max_tokens:
            chunks.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        chunks.append(" ".join(cur))
    return chunks

def split_into_chunks_iter(text: str, max_tokens: int):
    """
    Yield successive whitespace-delimited chunks of `text` with at most `max_tokens` tokens each.
    
    This is a generator version of chunking that splits input on whitespace (equivalent to `text.split()`) and yields each chunk as a single string of tokens joined by spaces. Raises ValueError if `max_tokens` is not positive.
    
    Parameters:
        max_tokens (int): Maximum number of tokens per yielded chunk; must be > 0.
    
    Yields:
        str: Next chunk containing 1..max_tokens tokens (empty input yields nothing).
    
    Raises:
        ValueError: If `max_tokens <= 0`.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    cur: list[str] = []
    for w in text.split():
        if len(cur) + 1 > max_tokens:
            yield " ".join(cur)
            cur = [w]
        else:
            cur.append(w)
    if cur:
        yield " ".join(cur)

if __name__ == "__main__":
    demo = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda"
    print(count_tokens(demo))
    print(split_into_chunks(demo, 3))
