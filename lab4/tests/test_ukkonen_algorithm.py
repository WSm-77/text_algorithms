import pytest
import os

from lab4.ukkonen_algorithm import SuffixTree

class TestSuffixTree:
    texts = ["abcabx",
             "abcabxabd",
             "abcabxabcd",
             "banan",
             "niedzwiedzdzwiedz"
             "x" * 100,
             "ab" * 100 + "x"]

    def test_build_tree_single_words(self):

        for text in TestSuffixTree.texts:
            trie = SuffixTree(text)
            assert len(trie.text) == len(trie)

    def test_build_tree_texts(self):
        texts_dir = "texts"
        path_to_dir = os.path.join(os.path.dirname(__file__), texts_dir)

        for file_path in os.listdir(path_to_dir):
            full_file_path = os.path.join(path_to_dir, file_path)
            with open(full_file_path, "r") as file:
                text = file.read()
                trie = SuffixTree(text)
                assert len(trie.text) == len(trie)

    def test_find_pattern_basic(self):
        text = "ABABCABCABC"
        pattern = "ABC"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = [2, 5, 8]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_find_pattern_multiple_matches(self):
        text = "ABABABABABA"
        pattern = "ABA"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = [0, 2, 4, 6, 8]
        assert sorted(result) == sorted(expected), f"Oczekiwano: {expected}, otrzymano: {result}"

    def test_find_pattern_no_match(self):
        text = "ABCDEF"
        pattern = "XYZ"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_empty_pattern(self):
        text = "ABCDEF"
        pattern = ""
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_empty_text(self):
        text = ""
        pattern = "ABC"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_pattern_equals_text(self):
        text = "ABC"
        pattern = "ABC"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = [0]
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"

    def test_find_pattern_pattern_longer_than_text(self):
        text = "ABC"
        pattern = "ABCDEF"
        trie = SuffixTree(text)
        result = trie.find_pattern(pattern)
        expected = []
        assert sorted(result) == sorted(expected), f"Expected: {expected}, got: {result}"
