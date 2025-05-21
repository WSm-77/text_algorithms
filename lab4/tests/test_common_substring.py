import pytest
from lab4.common_substring import longest_common_substring, longest_common_substring_multiple

class TestLCS:
    def test_basic_overlap(self):
        assert longest_common_substring("banana", "ananas") == "anana"

    def test_no_overlap(self):
        assert longest_common_substring("abc", "xyz") == ""

    def test_full_match(self):
        assert longest_common_substring("hello", "hello") == "hello"

    def test_empty_strings(self):
        assert longest_common_substring("", "") == ""
        assert longest_common_substring("abc", "") == ""
        assert longest_common_substring("", "abc") == ""

    def test_multiple_common_substrings(self):
        # Both "abc" and "bca" are common, but "abc" appears first
        assert longest_common_substring("abcabc", "bcaabc") in {"abc", "bca"}

    def test_case_sensitivity(self):
        assert longest_common_substring("ABC", "abc") == ""

    def test_longest_at_end(self):
        assert longest_common_substring("xyzabc", "defabc") == "abc"

    def test_longest_at_start(self):
        assert longest_common_substring("abcdef", "abcxyz") == "abc"

class TestLCSMultiple:
    def test_basic_overlap(self):
        assert longest_common_substring_multiple(["banana", "ananas", "canada"]) == "ana"

    def test_no_common_substring(self):
        assert longest_common_substring_multiple(["abc", "def", "ghi"]) == ""

    def test_full_match(self):
        assert longest_common_substring_multiple(["hello", "hello", "hello"]) == "hello"

    def test_empty_strings(self):
        assert longest_common_substring_multiple(["", "abc", "def"]) == ""
        assert longest_common_substring_multiple(["", "", ""]) == ""

    def test_common_at_end(self):
        assert longest_common_substring_multiple(["xyzabc", "defabc", "123abc"]) == "abc"

    def test_common_at_start(self):
        assert longest_common_substring_multiple(["abcdef", "abcxyz", "abcpqr"]) == "abc"

    def test_case_sensitivity(self):
        assert longest_common_substring_multiple(["ABC", "abc", "Abc"]) == ""

    def test_multiple_candidates(self):
        # Both "ab" and "bc" are common, but "ab" appears first in all
        assert longest_common_substring_multiple(["abxcaxbc", "zabcz", "12abc34"]) in {"ab", "bc"}

    def test_overlap_a_lot_of_texts(self):
        assert longest_common_substring_multiple(["banana", "ananas", "canada", "kanapa", "x" * 8 + "ana" + "x" * 8]) == "ana"
