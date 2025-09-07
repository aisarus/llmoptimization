import pytest

try:
    from text_stats import count_tokens, split_into_chunks
except ModuleNotFoundError:
    from efmcalc.text_stats import count_tokens, split_into_chunks


def test_count_tokens():
    assert count_tokens("") == 0  # noqa: S101
    assert count_tokens("a b  c") == 3  # noqa: S101


def test_split_into_chunks_happy():
    text = "a b c d e f"
    assert split_into_chunks(text, 2) == ["a b", "c d", "e f"]  # noqa: S101


def test_split_into_chunks_invalid():
    with pytest.raises(ValueError):
        split_into_chunks("a b", 0)