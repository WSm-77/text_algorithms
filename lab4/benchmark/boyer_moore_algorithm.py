def compute_bad_character_table(pattern: str) -> dict:
    rightmost_occurences = {}
    for i, char in enumerate(pattern):
        rightmost_occurences[char] = i

    return rightmost_occurences

def compute_good_suffix_table(pattern: str) -> tuple[list[int], int]:
    pattern_len = len(pattern)
    good_suffix_table = [0] * (pattern_len + 1)
    border_pos = [0] * (pattern_len + 1)

    i = pattern_len
    j = pattern_len + 1
    border_pos[i] = j

    char_cmp_cnt = 0

    while i > 0:
        char_cmp_cnt += 1
        while j <= pattern_len and pattern[i - 1] != pattern[j - 1]:
            char_cmp_cnt += 1
            if good_suffix_table[j] == 0:
                good_suffix_table[j] = j - i
            j = border_pos[j]
        i -= 1
        j -= 1
        border_pos[i] = j

    j = border_pos[0]
    for i in range(pattern_len + 1):
        if good_suffix_table[i] == 0:
            good_suffix_table[i] = j
        if i == j:
            j = border_pos[j]

    return good_suffix_table, char_cmp_cnt

def boyer_moore_pattern_match(text: str, pattern: str) -> tuple[list[int], int]:
    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return [], 0

    bad_char_table = compute_bad_character_table(pattern)
    good_suffix_table, char_cmp_cnt = compute_good_suffix_table(pattern)
    char_cmp_cnt += len(pattern) # add comparisions from 'compute_bad_character_table(pattern)' call

    result = []
    i = 0

    while i <= text_len - pattern_len:
        j = pattern_len - 1

        char_cmp_cnt += 1
        while j >= 0 and pattern[j] == text[i + j]:
            char_cmp_cnt += 1
            j -= 1

        if j < 0:
            result.append(i)

            i += good_suffix_table[0]
        else:
            bad_char_shift = j - bad_char_table.get(text[i + j], -1)
            good_suffix_shift = good_suffix_table[j + 1]
            i += max(bad_char_shift, good_suffix_shift)

    return result, char_cmp_cnt
