from lab5.ukkonen_algorithm import SuffixTree, Node
from lab5.suffix_array import SuffixArray

class UniqueCharGenerator:
    def __init__(self):
        self.offset = 0

    def __next__(self):
        char = chr(128 + self.offset)
        self.offset += 1
        return char

def check_if_contains_all_classyfication_bits(classyfication: int, strings_cnt: int):
    for _ in range(strings_cnt):
        if (classyfication & 1 == 0):
            return False

        classyfication >>= 1

    return True

def longest_common_substring(str1: str, str2: str) -> str:
    """
    Find the longest common substring of two strings using a suffix tree.

    Args:
        str1: First string
        str2: Second string

    Returns:
        The longest common substring
    """

    def get_node_classification(node: Node, text_depth: int = 0) -> int:
        nonlocal str1_len, trie, max_height, substring_start_idx

        if not node.children:
            # return 2 ** (index of string in combined string) to allow bitwise or classification
            if node.id < str1_len:
                return 1 << 0
            else:
                return 1 << 1

        classyfication = 0

        for child_node in node.children.values():
            child_node_width = child_node.width()
            bits = get_node_classification(child_node, text_depth + child_node_width)
            classyfication |= bits

        if check_if_contains_all_classyfication_bits(classyfication, 2):
            if max_height < text_depth:
                max_height = text_depth
                substring_start_idx = node.end.value - text_depth + 1

        return classyfication

    # Concatenate the strings with a unique separator
    combined = str1 + "#" + str2

    # Build a suffix tree for the combined string
    trie = SuffixTree(combined)

    str1_len = len(str1) + 1
    max_height = 0
    substring_start_idx = 0

    # Traverse the tree to find the longest path that occurs in both strings
    root_classifiaction = get_node_classification(trie.root)

    if not check_if_contains_all_classyfication_bits(root_classifiaction, 2):
        return ""

    lcs = combined[substring_start_idx:substring_start_idx + max_height]

    return lcs

def longest_common_substring_multiple(strings: list[str]) -> str:
    """
    Find the longest common substring among multiple strings using suffix structures.

    Args:
        strings: List of strings to compare

    Returns:
        The longest common substring that appears in all strings
    """

    def get_node_classification(node: Node, text_depth: int = 0) -> int:
        nonlocal string_sizes, trie, max_height, substring_start_idx

        if not node.children:
            # return 2 ** (index of string in combined string) to allow bitwise or classification
            for str_idx, size in enumerate(string_sizes):
                if node.id < size:
                    return 1 << str_idx

            raise Exception("Should never happen")

        classyfication = 0

        for child_node in node.children.values():
            child_node_width = child_node.width()
            bits = get_node_classification(child_node, text_depth + child_node_width)
            classyfication |= bits

        if check_if_contains_all_classyfication_bits(classyfication, len(strings)):
            if max_height < text_depth:
                max_height = text_depth
                substring_start_idx = node.end.value - text_depth + 1

        return classyfication

    if len(strings) == 0:
        return ""

    # Concatenate the strings with a unique separator
    combined = strings[0]
    gen = UniqueCharGenerator()

    string_sizes = [len(strings[0]) + 1]

    for idx in range(1, len(strings)):
        string = strings[idx]
        combined += next(gen) + string

        string_sizes.append(len(combined) + 1)

    # Build a suffix tree for the combined string
    trie = SuffixTree(combined)

    max_height = 0
    substring_start_idx = 0

    # Traverse the tree to find the longest path that occurs in all strings
    root_classifiaction = get_node_classification(trie.root)

    if not check_if_contains_all_classyfication_bits(root_classifiaction, len(strings)):
        return ""

    lcs = combined[substring_start_idx:substring_start_idx + max_height]

    return lcs

def longest_palindromic_substring(text: str) -> str:
    """
    Find the longest palindromic substring in a given text using suffix structures.

    Args:
        text: Input text

    Returns:
        The longest palindromic substring
    """

    def get_node_classification(node: Node, text_depth: int = 0) -> int:
        nonlocal str1_len, trie, max_height, substring_start_idx

        if not node.children:
            # return 2 ** (index of string in combined string) to allow bitwise or classification
            if node.id < str1_len:
                forward_indices[node] = {node.id}
                reverse_indices[node] = set()
                return 1 << 0
            else:
                forward_indices[node] = set()
                reverse_indices[node] = {node.id - str1_len}
                return 1 << 1

        classyfication = 0

        forward_indices[node] = set()
        reverse_indices[node] = set()

        for child_node in node.children.values():
            child_node_width = child_node.width()
            bits = get_node_classification(child_node, text_depth + child_node_width)
            classyfication |= bits
            forward_indices[node] |= forward_indices[child_node]
            reverse_indices[node] |= reverse_indices[child_node]

        # if check_if_contains_all_classyfication_bits(classyfication, 2):
        if max_height < text_depth and forward_indices[node] and reverse_indices[node]:
            for forward_idx in forward_indices[node]:
                reverse_idx = (str1_len - 2) - (forward_idx + text_depth - 1)

                if reverse_idx in reverse_indices[node]:
                    max_height = text_depth
                    substring_start_idx = node.end.value - text_depth + 1
                    break

        return classyfication

    str1 = text
    str2 = text[::-1]
    # Concatenate the strings with a unique separator
    combined = str1 + "#" + str2

    # Build a suffix tree for the combined string
    trie = SuffixTree(combined)

    str1_len = len(str1) + 1
    max_height = 0
    substring_start_idx = 0

    forward_indices = {}
    reverse_indices = {}

    # Traverse the tree to find the longest path that occurs in both strings
    get_node_classification(trie.root)

    lcs = combined[substring_start_idx:substring_start_idx + max_height]

    return lcs

def longest_common_substring_suffix_array(a, b, delimiter='#'):
    # Concatenate with delimiter
    combined = a + delimiter + b
    l1 = len(a)

    # Build suffix array (naive approach for clarity)
    suffix_array = SuffixArray(combined)

    # Compute LCP array using Kasai's algorithm
    n = len(suffix_array)
    rank = [0] * n
    for i in range(n):
        rank[suffix_array.suffixes[i]] = i

    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if rank[i] == 0:
            continue
        j = suffix_array.suffixes[rank[i] - 1]
        while i + h < n and j + h < n and combined[i + h] == combined[j + h]:
            h += 1
        lcp[rank[i] - 1] = h
        if h > 0:
            h -= 1

    # Find maximum LCP across string boundaries
    max_len = 0
    start = 0
    for i in range(n - 1):
        idx1 = suffix_array.suffixes[i]
        idx2 = suffix_array.suffixes[i + 1]

        # Check if suffixes are from different original strings
        if (idx1 < l1) != (idx2 < l1) and lcp[i] > max_len:
            max_len = lcp[i]
            start = min(idx1, idx2)

    return combined[start:start + max_len] if max_len > 0 else ""
