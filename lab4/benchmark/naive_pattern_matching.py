def cmp_texts(text1, text2):
    if len(text1) != len(text2):
        return False, 0

    char_cmp_cnt = 0
    for i in range(len(text1)):
        char_cmp_cnt += 1
        if text1[i] != text2[i]:
            return False, char_cmp_cnt

    return True, char_cmp_cnt

def naive_pattern_match(text: str, pattern: str) -> tuple[list[int], int]:
    text_len = len(text)
    pattern_len = len(pattern)
    char_cmp_cnt = 0

    if pattern_len == 0 or pattern_len > text_len:
        return [], 0

    result = []
    for i in range(text_len):
        # if text[i:min(i + pattern_len, text_len)] == pattern:
        are_the_same, common_prefix_length = cmp_texts(text[i:min(i + pattern_len, text_len)], pattern)
        char_cmp_cnt += common_prefix_length
        if are_the_same:
            result.append(i)

    return result, char_cmp_cnt
