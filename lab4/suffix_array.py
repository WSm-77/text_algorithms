from __future__ import annotations

def sorted_search(tab, val, key=lambda x: x, side = 'left'):
    beg, end = 0, len(tab) - 1
    while beg <= end:
        mid = (beg + end) // 2
        if val == key(tab[mid]):
            if side == 'left':
                end = mid - 1
            elif side == 'right':
                beg = mid + 1
            else:
                raise Exception(f"Incorrect side argument: {side}")
        elif val < key(tab[mid]):
            end = mid - 1
        else:
            beg = mid + 1
    return beg

class Suffix:
    def __init__(self, suffix: str, idx: int):
        self.suffix = suffix
        self.idx = idx

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
            return []

        key_function = lambda x: self.suffix(x)[:len(pattern)]
        il = sorted_search(self.suffixes, pattern, key = key_function, side = 'left')
        ir = sorted_search(self.suffixes, pattern, key = key_function, side = 'right')

        return self.suffixes[il:ir]

    def __len__(self):
        return len(self.suffixes)
