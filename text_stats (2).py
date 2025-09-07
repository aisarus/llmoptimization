from __future__ import annotations
from typing import List

def count_tokens(text: str) -> int:
    """
    Return the number of whitespace-separated tokens in `text`.
    
    This is an ultra-naive tokenizer that counts tokens by splitting on any whitespace. If `text` is empty or falsy, returns 0.
    """
    if not text:
        return 0
    return len(text.split())

def split_into_chunks(text: str, max_tokens: int) -> list[str]:
    """
    Split the input text into space-joined chunks, each containing at most `max_tokens` whitespace-separated tokens.
    
    Empty or whitespace-only input returns an empty list. `max_tokens` must be a positive integer or a ValueError is raised. Tokens are determined by str.split() (whitespace-separated); the returned chunks preserve original token order and join tokens with a single space.
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
    Yield successive whitespace-token chunks from `text`, each containing at most `max_tokens` tokens.
    
    This generator splits `text` on whitespace and yields chunk strings where each chunk's token count does not exceed `max_tokens`. If `text` contains no words, nothing is yielded. The final chunk (if non-empty) is yielded after iteration.
    
    Parameters:
        text (str): Input string to split.
        max_tokens (int): Maximum number of whitespace-separated tokens per yielded chunk; must be positive.
    
    Yields:
        str: Next chunk containing up to `max_tokens` tokens.
    
    Raises:
        ValueError: If `max_tokens` is not a positive integer.
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
