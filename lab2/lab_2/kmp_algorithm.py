def length_of_common_prefix(str1: str, str2: str) -> int:
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] != str2[i]:
            return i
    return min_len

def z_function(s: str):
    z = [0] * len(s)
    l = 0
    r = 0
    for k in range(1, len(s)):
        if k >= r:
            z[k] = length_of_common_prefix(s[k:], s)
            if z[k] > 0:
                l = k
                r = k + z[k]
        elif z[k - l] >= r - k:
            z[k] = r - k + length_of_common_prefix(s[r:], s[r - k:])
            l = k
            r = k + z[k]
        else:
            z[k] = z[k - l]

    return z

def compute_lps_array(pattern: str) -> list[int]:
    """
    Compute the Longest Proper Prefix which is also Suffix array for KMP algorithm.

    Args:
        pattern: The pattern string

    Returns:
        The LPS array
    """
    # TODO: Implement the Longest Prefix Suffix (LPS) array computation
    # The LPS array helps in determining how many characters to skip when a mismatch occurs
    # For each position i, compute the length of the longest proper prefix of pattern[0...i]
    # that is also a suffix of pattern[0...i]
    # Hint: Use the information from previously computed values to avoid redundant comparisons

    # pattern_len = len(pattern)
    # z_arr = compute_z_array(pattern)
    # lps_arr = [0] * (pattern_len + 1)

    # for i in range(pattern_len - 1, 0, -1):
    #     lps_arr[i + z_arr[i]] = z_arr[i]

    # return lps_arr
    lps = [0] * len(pattern)
    length = 0  # Length of the previous longest prefix suffix
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps

    # z = z_function(pattern)
    # p = [0] * (len(pattern) + 1)

    # for j in range(len(pattern) - 1, 0, -1):
    #      p[j + z[j]] = z[j]

    # return p

def kmp_pattern_match(text: str, pattern: str) -> list[int]:
    """
    Implementation of the Knuth-Morris-Pratt pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # Implement the KMP string matching algorithm
    # 1. Preprocess the pattern to compute the LPS array
    # 2. Use the LPS array to determine how much to shift the pattern when a mismatch occurs
    # 3. This avoids redundant comparisons by using information about previous matches
    # 4. Return all positions where the pattern is found in the text

    text_len = len(text)
    pattern_len = len(pattern)

    if text_len < pattern_len or pattern_len == 0:
        return []

    result = []

    p = compute_lps_array(pattern)
    j = 0
    for i in range(len(text)):
        while j > 0 and text[i] != pattern[j]:
            j = p[j - 1]

        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            result.append(i - len(pattern) + 1)
            j = p[j - 1]

    return result

if __name__ == "__main__":
    pattern = "ABABACA"
    res = compute_lps_array(pattern)
    print(res)
