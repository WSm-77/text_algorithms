def length_of_common_prefix(str1: str, str2: str) -> int:
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return i
    return min_len

def compute_z_array(s: str) -> list[int]:
    """
    Compute the Z array for a string.

    The Z array Z[i] gives the length of the longest substring starting at position i
    that is also a prefix of the string.

    Args:
        s: The input string

    Returns:
        The Z array for the string
    """
    # TODO: Implement the Z-array computation
    # For each position i:
    # - Calculate the length of the longest substring starting at i that is also a prefix of s
    # - Use the Z-box technique to avoid redundant character comparisons
    # - Handle the cases when i is inside or outside the current Z-box

    # str_len = len(s)

    # res = [length_of_common_prefix(s[i:], s) for i in range(str_len)]
    # res[0] = 0

    # return res

    z = [0] * len(s)

    for k in range(1, len(s)):
        z[k] = length_of_common_prefix(s[k:], s)

    return z

def z_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Use the Z algorithm to find all occurrences of a pattern in a text.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # TODO: Implement pattern matching using the Z algorithm

    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return []

    SPECIAL_CHAR = '\\'

    # 1. Create a concatenated string: pattern + special_character + text
    concatenated = pattern + SPECIAL_CHAR + text

    # 2. Compute the Z array for this concatenated string
    z_arr = compute_z_array(concatenated)

    # 3. Find positions where Z[i] equals the pattern length
    found_positions = [i for i, z_val in enumerate(z_arr) if z_val == pattern_len]

    # 4. Convert these positions in the concatenated string to positions in the original text
    converted_positions = [pos - len(SPECIAL_CHAR) - pattern_len for pos in found_positions]

    # 5. Return all positions where the pattern is found in the text
    return converted_positions
