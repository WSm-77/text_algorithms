def hash_byte(curr_hash: int, byte: int, mod: int = 101):
    return (curr_hash + byte) % mod

def unhash_byte(curr_hash: int, byte: int, mod: int = 101):
    return (curr_hash - byte + mod) % mod

def hash_string(substr: str, mod: int = 101):
    hash_res = 0
    for char in substr:
        hash_res = hash_byte(hash_res, ord(char), mod)

    return hash_res

def rabin_karp_pattern_match(text: str, pattern: str, prime: int = 101) -> list[int]:
    """
    Implementation of the Rabin-Karp pattern matching algorithm.

    Args:
        text: The text to search in
        pattern: The pattern to search for
        prime: A prime number used for the hash function

    Returns:
        A list of starting positions (0-indexed) where the pattern was found in the text
    """
    # Implement the Rabin-Karp string matching algorithm
    # This algorithm uses hashing to find pattern matches:
    # 1. Compute the hash value of the pattern
    # 2. Compute the hash value of each text window of length equal to pattern length
    # 3. If the hash values match, verify character by character to avoid hash collisions
    # 4. Use rolling hash to efficiently compute hash values of text windows
    # 5. Return all positions where the pattern is found in the text
    # Note: Use the provided prime parameter for the hash function to avoid collisions

    result = []
    text_len = len(text)
    pattern_len = len(pattern)

    if pattern_len == 0 or text_len < pattern_len:
        return []

    pattern_hash = hash_string(pattern, prime)
    curr_hash = hash_string(text[:pattern_len], prime)

    i = 0
    while True:
        if curr_hash == pattern_hash and text[i:i+pattern_len] == pattern:
            result.append(i)

        if text_len <= i + pattern_len:
            break

        curr_hash = hash_byte(curr_hash, ord(text[i+pattern_len]))
        curr_hash = unhash_byte(curr_hash, ord(text[i]), prime)

        i += 1

    return result
