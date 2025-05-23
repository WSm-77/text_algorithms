def cmp_texts(text1, text2):
    if len(text1) != len(text2):
        return False, 0

    char_cmp_cnt = 0
    for i in range(len(text1)):
        char_cmp_cnt += 1
        if text1[i] != text2[i]:
            return False, char_cmp_cnt

    return True, char_cmp_cnt

def hash_byte(curr_hash: int, byte: int, mod: int = 101):
    return (curr_hash + byte) % mod

def unhash_byte(curr_hash: int, byte: int, mod: int = 101):
    return (curr_hash - byte + mod) % mod

def hash_string(substr: str, mod: int = 101):
    hash_res = 0
    for char in substr:
        hash_res = hash_byte(hash_res, ord(char), mod)

    return hash_res

def rabin_karp_pattern_match(text: str, pattern: str, prime: int = 101) -> tuple[list[int], int]:
    result = []
    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return [], 0

    pattern_hash = hash_string(pattern, prime)
    curr_hash = hash_string(text[:pattern_len], prime)

    char_cmp_cnt = 0

    i = 0
    while True:
        if curr_hash == pattern_hash and text[i:i+pattern_len] == pattern:
            are_the_same, common_prefix_length = cmp_texts(text[i:i+pattern_len], pattern)
            char_cmp_cnt += common_prefix_length
            if are_the_same:
                result.append(i)

        if text_len <= i + pattern_len:
            break

        curr_hash = hash_byte(curr_hash, ord(text[i+pattern_len]))
        curr_hash = unhash_byte(curr_hash, ord(text[i]), prime)

        i += 1

    return result, char_cmp_cnt
