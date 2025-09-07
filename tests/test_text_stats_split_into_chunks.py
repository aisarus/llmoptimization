import importlib
import inspect
import types

import pytest


def _import_text_stats():
    mod = importlib.import_module("efmcalc.text_stats")
    if not isinstance(mod, types.ModuleType):
        pytest.fail(f"Expected efmcalc.text_stats to be a module, got {type(mod)}")
    return mod


def test_split_into_chunks_public_api_exists_and_has_doc():
    ts = _import_text_stats()
    if not hasattr(ts, "split_into_chunks"):
        pytest.fail("split_into_chunks not found in text_stats module")
    fn = ts.split_into_chunks
    if not callable(fn):
        pytest.fail("split_into_chunks should be callable")
    if not inspect.getdoc(fn):
        pytest.fail("split_into_chunks should have a docstring")


@pytest.mark.parametrize(
    "text, size, expected_count",
    [
        ("", 10, 0),              # empty input -> no chunks
        ("abc", 1, 3),            # exact single-char chunks
        ("abc", 2, 2),            # "ab","c"
        ("abc", 3, 1),            # "abc"
        ("abc", 5, 1),            # size greater than len -> single chunk
        ("a"*100, 10, 10),        # many equal chunks
        ("a"*101, 10, 11),        # last chunk partial
    ],
)
def test_split_into_chunks_basic_counts(text, size, expected_count):
    ts = _import_text_stats()
    chunks = ts.split_into_chunks(text, size)
    if not isinstance(chunks, (list, tuple)):
        pytest.fail(f"Expected list or tuple of chunks, got {type(chunks)}")
    if len(chunks) != expected_count:
        pytest.fail(f"Expected {expected_count} chunks, got {len(chunks)}")
    for ch in chunks:
        if not isinstance(ch, str):
            pytest.fail(f"Chunk {ch!r} is not a string")
        if not (0 < len(ch) <= max(1, size)):
            pytest.fail(f"Chunk length {len(ch)} is not within the valid range for size {size}")


def test_split_into_chunks_whitespace_and_newlines_are_preserved_or_handled():
    ts = _import_text_stats()
    text = "Hello\nworld\tthis is  spaced"
    chunks = ts.split_into_chunks(text, 5)
    if not all(isinstance(c, str) for c in chunks):
        pytest.fail("Not all chunks are strings")
    if "".join(chunks) != text:
        pytest.fail("Concatenation of chunks should reconstruct original text when naive chunking")


@pytest.mark.parametrize("bad_size", [0, -1, -10, None, 1.5, "10"])
def test_split_into_chunks_invalid_size(bad_size):
    ts = _import_text_stats()
    text = "hello world"
    if isinstance(bad_size, int) and bad_size > 0:
        pytest.skip("valid size")
    with pytest.raises((ValueError, TypeError)):
        ts.split_into_chunks(text, bad_size)  # type: ignore[arg-type]


def test_split_into_chunks_non_string_input_graceful():
    ts = _import_text_stats()
    with pytest.raises((TypeError, ValueError)):
        ts.split_into_chunks(None, 5)  # type: ignore[arg-type]
    with pytest.raises((TypeError, ValueError)):
        ts.split_into_chunks(123, 5)   # type: ignore[arg-type]