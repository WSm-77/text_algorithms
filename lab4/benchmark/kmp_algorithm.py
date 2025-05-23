def compute_lps_array(pattern: str) -> tuple[list[int], int]:
    lps = [0] * len(pattern)
    length = 0  # Length of the previous longest prefix suffix
    i = 1

    char_cmp_count = 0

    while i < len(pattern):
        char_cmp_count += 1
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

    return lps, char_cmp_count

def kmp_pattern_match(text: str, pattern: str) -> tuple[list[int], int]:
    text_len = len(text)
    pattern_len = len(pattern)

    if text_len < pattern_len or pattern_len == 0:
        return [], 0

    result = []

    p, char_cmp_count = compute_lps_array(pattern)
    j = 0

    for i in range(len(text)):
        char_cmp_count += 1
        while j > 0 and text[i] != pattern[j]:
            char_cmp_count += 1
            j = p[j - 1]

        char_cmp_count += 1
        if text[i] == pattern[j]:
            j += 1

        if j == len(pattern):
            result.append(i - len(pattern) + 1)
            j = p[j - 1]

    return result, char_cmp_count
