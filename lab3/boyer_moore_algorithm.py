def compute_bad_character_table(pattern: str) -> dict:
    """
    Compute the bad character table for the Boyer-Moore algorithm.

    Args:
        pattern: The pattern string

    Returns:
        A dictionary with keys as characters and values as the rightmost position
        of the character in the pattern (0-indexed)
    """
    # Implement the bad character heuristic for Boyer-Moore algorithm
    # This table maps each character to its rightmost occurrence in the pattern
    # For characters not in the pattern, they should not be in the dictionary
    # Remember that this is used to determine how far to shift when a mismatch occurs

    rightmost_occurences = {}
    for i, char in enumerate(pattern):
        rightmost_occurences[char] = i

    return rightmost_occurences


def compute_good_suffix_table(pattern: str) -> list[int]:
    """
    Compute the good suffix table for the Boyer-Moore algorithm.

    Args:
        pattern: The pattern string

    Returns:
        A list where shift[i] stores the shift required when a mismatch
        happens at position i of the pattern
    """
    # Implement the good suffix heuristic for Boyer-Moore algorithm
    # This is a more complex rule that handles:
    # 1. When we have seen a suffix before elsewhere in the pattern
    # 2. When only a prefix of the suffix matches a prefix of the pattern
    # Hint: This involves two-phase preprocessing of the pattern

    pattern_len = len(pattern)
    good_suffix_table = [0] * (pattern_len + 1)
    border_pos = [0] * (pattern_len + 1)

    # Phase 1: Compute border positions
    i = pattern_len
    j = pattern_len + 1
    border_pos[i] = j

    while i > 0:
        while j <= pattern_len and pattern[i - 1] != pattern[j - 1]:
            if good_suffix_table[j] == 0:
                good_suffix_table[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    # Phase 2: Fill in the good suffix table
    j = border_pos[0]
    for i in range(pattern_len + 1):
        if good_suffix_table[i] == 0:
            good_suffix_table[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix_table


def boyer_moore_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Boyer-Moore pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # Implement the Boyer-Moore string matching algorithm
    # 1. Preprocess the pattern to create the bad character and good suffix tables
    # 2. Start matching from the end of the pattern and move backwards
    # 3. When a mismatch occurs, use the maximum shift from both tables
    # 4. Return all positions where the pattern is found in the text

    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return []

    bad_char_table = compute_bad_character_table(pattern)
    good_suffix_table = compute_good_suffix_table(pattern)

    result = []
    i = 0

    while i <= text_len - pattern_len:
        j = pattern_len - 1

        # Match the pattern from right to left
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1

        if j < 0:
            # Pattern found at position i
            result.append(i)

            # Shift by the value in the good suffix table
            i += good_suffix_table[0]
        else:
            # Calculate the shift using both heuristics
            bad_char_shift = j - bad_char_table.get(text[i + j], -1)
            good_suffix_shift = good_suffix_table[j + 1]
            i += max(bad_char_shift, good_suffix_shift)

    return result
