from __future__ import annotations

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

    def __len__(self):
        return len(self.suffixes)
