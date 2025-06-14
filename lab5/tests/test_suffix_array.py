import pytest
from lab5.suffix_array import SuffixArray

class TestSuffixArrayFindPattern:
    def test_find_pattern_basic(self):
        text = "ABABCABCABC"
        pattern = "ABC"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = [2, 5, 8]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_find_pattern_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = [0, 2, 4, 6, 8]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_find_pattern_no_match(self):
        text = "ABCDEF"
        pattern = "XYZ"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_empty_pattern(self):
        text = "ABCDEF"
        pattern = ""
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_empty_text(self):
        text = ""
        pattern = "ABC"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_pattern_equals_text(self):
        text = "ABC"
        pattern = "ABC"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = [0]
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_pattern_longer_than_text(self):
        text = "ABC"
        pattern = "ABCDEF"
        suff_array = SuffixArray(text)
        result = suff_array.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"
