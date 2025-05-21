import pytest
import os

from lab4.ukkonen_algorithm import SuffixTree

class TestSuffixTree:
    def test_build_tree_single_words(self):
        texts = ["abcabx",
                 "abcabxabd",
                 "abcabxabcd",
                 "banan",
                 "niedzwiedzdzwiedz"
                 "x" * 100,
                 "ab" * 100 + "x"]

        for text in texts:
            trie = SuffixTree(text)
            assert len(trie.text) == trie.count_suffixes()

    def test_build_tree_texts(self):
        texts_dir = "texts"
        path_to_dir = os.path.join(os.path.dirname(__file__), texts_dir)

        for file_path in os.listdir(path_to_dir):
            full_file_path = os.path.join(path_to_dir, file_path)
            with open(full_file_path, "r") as file:
                text = file.read()
                trie = SuffixTree(text)
                assert len(trie.text) == trie.count_suffixes()
