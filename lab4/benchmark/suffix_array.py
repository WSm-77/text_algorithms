from __future__ import annotations

def compare_strings(str1, str2):
    comparisons = 0
    min_len = min(len(str1), len(str2))

    for i in range(min_len):
        comparisons += 1
        if str1[i] < str2[i]:
            return -1, comparisons
        elif str1[i] > str2[i]:
            return 1, comparisons

    if len(str1) < len(str2):
        return -1, comparisons + 1
    elif len(str1) > len(str2):
        return 1, comparisons + 1
    else:
        return 0, comparisons

def sorted_search(tab, val, key=lambda x: x, side = 'left'):
    beg, end = 0, len(tab) - 1
    char_cmp_cnt = 0
    while beg <= end:
        mid = (beg + end) // 2
        cmp, common_prefix_length = compare_strings(val, key(tab[mid]))
        if cmp == 0:
            if side == 'left':
                end = mid - 1
            elif side == 'right':
                beg = mid + 1
            else:
                raise Exception(f"Incorrect side argument: {side}")
        elif cmp == -1:
            end = mid - 1
        else:
            beg = mid + 1
    return beg, char_cmp_cnt

class Suffix:
    def __init__(self, suffix: str, idx: int):
        self.suffix = suffix
        self.idx = idx

    def __repr__(self):
        return self.suffix

class SuffixArray:
    def __init__(self, text: str) -> None:
        self.suffixes = [0] * len(text)
        self.text = text
        self.build()

    def build(self):
        suffixes = [Suffix(self.text[idx:], idx) for idx in range(len(self.text))]
        suffixes.sort(key = lambda suff: suff.suffix)

        for i, suff in enumerate(suffixes):
            self.suffixes[i] = suff.idx

    def suffix(self, idx: int):
        return self.text[idx:]

    def find_pattern(self, pattern: str):
        if len(pattern) == 0:
            return [], 0

        key_function = lambda x: self.suffix(x)[:len(pattern)]
        il, char_cmp_cnt = sorted_search(self.suffixes, pattern, key = key_function, side = 'left')
        ir, cmp_cnt = sorted_search(self.suffixes, pattern, key = key_function, side = 'right')
        char_cmp_cnt += cmp_cnt

        return self.suffixes[il:ir], char_cmp_cnt

    def __len__(self):
        return len(self.suffixes)
