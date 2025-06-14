def naive_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the naive pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # Implement the naive pattern matching algorithm
    # This is the most straightforward approach to string matching:
    # 1. Check every possible starting position in the text
    # 2. For each position, compare the pattern with the text character by character
    # 3. If all characters match, add the starting position to the results
    # 4. Handle edge cases like empty patterns and patterns longer than the text

    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or pattern_len > text_len:
        return []

    result = []
    for i in range(text_len):
        if text[i:min(i + pattern_len, text_len)] == pattern:
            result.append(i)

    return result
