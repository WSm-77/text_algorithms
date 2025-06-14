def longest_common_substring(a, b, delimiter='#'):
    # Step 1: Concatenate with delimiter
    combined = a + delimiter + b
    l1 = len(a)

    # Step 2: Build suffix array (naive approach for clarity)
    suffixes = sorted([(combined[i:], i) for i in range(len(combined))], key=lambda x: x[0])
    sa = [idx for (suf, idx) in suffixes]

    # Step 3: Compute LCP array using Kasai's algorithm
    n = len(sa)
    rank = [0] * n
    for i in range(n):
        rank[sa[i]] = i

    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if rank[i] == 0:
            continue
        j = sa[rank[i] - 1]
        while i + h < n and j + h < n and combined[i + h] == combined[j + h]:
            h += 1
        lcp[rank[i] - 1] = h
        if h > 0:
            h -= 1

    # Step 4: Find maximum LCP across string boundaries
    max_len = 0
    start = 0
    for i in range(n - 1):
        idx1 = sa[i]
        idx2 = sa[i + 1]
        # Check if suffixes are from different original strings
        if (idx1 < l1) != (idx2 < l1) and lcp[i] > max_len:
            max_len = lcp[i]
            start = min(idx1, idx2)

    return combined[start:start + max_len] if max_len > 0 else ""

if __name__ == "__main__":
    text1 = "ananas"
    text2 = "bananowy"
    res = longest_common_substring(text1, text2)
    print(res)
