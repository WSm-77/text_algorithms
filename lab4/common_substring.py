# from lab4.ukkonen_algorithm import SuffixTree, Node
from ukkonen_algorithm import SuffixTree, Node

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

    # Create a new string concatenating the original text and its reverse
    # Use suffix structures to find the longest common substring between them
    # Handle the case where palindrome centers between characters

    def get_node_classification(node: Node, text_depth: int = 0) -> int:
        nonlocal max_len, start_idx

        if not node.children:
            # Return 1 if suffix starts in original text, 2 if in reversed
            if node.id < n:
                return 1
            elif node.id > n:
                return 2
            else:
                return 0  # Separator
        classyfication = 0
        for child in node.children.values():
            child_width = child.width()
            bits = get_node_classification(child, text_depth + child_width)
            classyfication |= bits

        # If this node is present in both original and reversed text
        if classyfication == 3 and text_depth > max_len:
            # Find the start index in the original text
            # node.end.value - text_depth + 1 is the start in combined string
            candidate_start = node.end.value - text_depth + 1
            if candidate_start < n:
                # Check if the substring is a palindrome
                candidate = combined[candidate_start:candidate_start + text_depth]
                if candidate == candidate[::-1]:
                    max_len = text_depth
                    start_idx = candidate_start

        return classyfication

    if not text:
        return ""

    # Concatenate text and its reverse with a unique separator
    sep = chr(128)
    reversed_text = text[::-1]
    combined = text + sep + reversed_text

    # Build a suffix tree for the combined string
    trie = SuffixTree(combined)
    n = len(text)

    max_len = 0
    start_idx = 0

    get_node_classification(trie.root)

    return text[start_idx:start_idx + max_len]

if __name__ == "__main__":
    # str1 = "ananas"
    # str2 = "banan"
    # str1 = "ananas"
    # str2 = "kot"
    # lcs = longest_common_substring(str1, str2)
    # str3 = "kanapa"
    # str4 = "anna"
    # lcs = longest_common_substring_multiple([str1, str2, str3, str4])
    # print(lcs)

    text = "xababayz"
    lps = longest_palindromic_substring(text)
    print(f"lps of '{text}' is '{lps}'")

    text = "abacdfgdcaba"
    lps = longest_palindromic_substring(text)
    print(f"lps of '{text}' is '{lps}'")

    text = "pqrqpabcdfgdcba"
    lps = longest_palindromic_substring(text)
    print(f"lps of '{text}' is '{lps}'")

    text = "pqqpabcdfghfdcba"
    lps = longest_palindromic_substring(text)
    print(f"lps of '{text}' is '{lps}'")

    # gen = UniqueCharGenerator()
