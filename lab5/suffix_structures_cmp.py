from lab5.suffix_array import SuffixArray
from lab5.ukkonen_algorithm import SuffixTree
from typing import Callable
import time
from memory_profiler import memory_usage

def measure_params(func: Callable[[str], object], *func_args) -> dict[str, float]:
    start_time = time.perf_counter()
    mem_usage, obj = memory_usage((func, func_args), retval=True)
    end_time = time.perf_counter()

    return {
            "construction_time_ms": (end_time - start_time) * 1000,
            "memory_usage_kb": (max(mem_usage) - min(mem_usage)) * 1024,
            "size": len(obj)
           }


def compare_suffix_structures(text: str) -> dict:
    """
    Compare suffix array and suffix tree data structures.

    Args:
        text: The input text for which to build the structures

    Returns:
        A dictionary containing:
        - Construction time for both structures
        - Memory usage for both structures
        - Size (number of nodes/elements) of both structures
    """

    return {
        "suffix_array": measure_params(SuffixArray, text),
        "suffix_tree": measure_params(SuffixTree, text)
    }
