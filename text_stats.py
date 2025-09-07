from typing import List

def count_tokens(text: str) -> int:
    """Ultra-naive token counter: split by whitespace.

    This is deliberately simple; reviewers can suggest using a real tokenizer.
    """
    if not text:
        return 0
    return len(text.split())


def split_into_chunks(text: str, max_tokens: int) -> List[str]:
    """Split text into chunks with at most `max_tokens` tokens each.

    Args:
        text: source text.
        max_tokens: positive integer, the soft limit per chunk.

    Returns:
        List of chunk strings.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be positive")
    words = text.split()
    if not words:
        return []
    chunks: List[str] = []
    cur: List[str] = []
    for w in words:
        if len(cur) + 1 > max_tokens:
            chunks.append(" ".join(cur))
            cur = [w]
        else:
            cur.append(w)
    if cur:
        chunks.append(" ".join(cur))
    return chunks


if __name__ == "__main__":
    # Simple demo
    demo = "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda"
    print(count_tokens(demo))
    print(split_into_chunks(demo, 3))
