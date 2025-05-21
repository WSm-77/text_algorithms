import pytest
from lab4.common_substring import longest_common_substring

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
