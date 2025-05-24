import time
from memory_profiler import memory_usage
from typing import Callable
from lab4.benchmark.naive_pattern_matching import naive_pattern_match
from lab4.benchmark.kmp_algorithm import kmp_pattern_match
from lab4.benchmark.boyer_moore_algorithm import boyer_moore_pattern_match
from lab4.benchmark.rabin_karp_algorithm import rabin_karp_pattern_match
from lab4.benchmark.aho_corasick_algorithm import AhoCorasick
from lab4.benchmark.suffix_array import SuffixArray
from lab4.benchmark.ukkonen_algorithm import SuffixTree


def compare_pattern_matching_algorithms(text: str, pattern: str) -> dict:
    """
    Compare the performance of different pattern matching algorithms.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A dictionary containing the results of each algorithm:
        - Execution time in milliseconds
        - Memory usage in kilobytes
        - Number of character comparisons made
        - Positions where the pattern was found
    """
    def measure_params(func: Callable[[str, str], tuple[list[int], int]] | Callable[[str], tuple[list[int], int]], *func_args) -> dict[str, float]:
        start_time = time.perf_counter()
        mem_usage, res = memory_usage((func, func_args), retval=True)
        end_time = time.perf_counter()
        pattern_found, char_cmp_cnt = res

        return {
            "exec_time": (end_time - start_time) * 1000,
            "mem_usage": (max(mem_usage) - min(mem_usage)) * 1024,
            "char_cmp_cnt": char_cmp_cnt,
            "pattern_found": pattern_found
        }

    args = text, pattern

    aho_corasick = AhoCorasick([pattern])
    suff_arr = SuffixArray(text)
    suff_tree = SuffixTree(text)

    return {
        "naive": measure_params(naive_pattern_match, *args),
        "kmp": measure_params(kmp_pattern_match, *args),
        "boyer-moore": measure_params(boyer_moore_pattern_match, *args),
        "rabin-karp": measure_params(rabin_karp_pattern_match, *args),
        "aho-corasick": measure_params(aho_corasick.search, text),
        "suffix-array": measure_params(suff_arr.find_pattern, pattern),
        "suffix-tree": measure_params(suff_tree.find_pattern, pattern),
    }
