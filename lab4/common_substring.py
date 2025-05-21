from lab4.ukkonen_algorithm import SuffixTree, Node

def longest_common_substring(str1: str, str2: str) -> str:
    """
    Find the longest common substring of two strings using a suffix tree.

    Args:
        str1: First string
        str2: Second string

    Returns:
        The longest common substring
    """

    def check_if_contains_all_classyfication_bits(classyfication: int, strings_cnt: int):
        for _ in range(strings_cnt):
            if (classyfication & 1 == 0):
                return False

            classyfication >>= 1

        return True

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
    # Traverse the tree to find the longest path that occurs in both strings

    trie = SuffixTree(combined)

    str1_len = len(str1) + 1
    max_height = 0
    substring_start_idx = 0

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
    # Implement an algorithm to find the longest common substring in multiple strings
    # You may use either suffix trees or suffix arrays

    pass

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

    pass

if __name__ == "__main__":
    # str1 = "ananas"
    # str2 = "banan"
    str1 = "ananas"
    str2 = "kot"
    lcs = longest_common_substring(str1, str2)
    print(lcs)
