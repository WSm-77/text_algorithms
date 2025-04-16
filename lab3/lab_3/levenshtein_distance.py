def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Levenshteina między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Levenshteina (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    # Zaimplementuj obliczanie odległości Levenshteina
    # Obsłuż przypadki brzegowe (puste ciągi)
    # Zaimplementuj algorytm dynamicznego programowania do obliczenia odległości

    sourceLen = len(s1)
    targetLen = len(s2)

    # dp[i][j] - distance between strings s1[:i] and s2[:j]
    dp = [[None for _ in range(targetLen+1)] for _ in range(sourceLen+1)]

    def backtrack(i, j):
        if dp[i][j] != None:
            return dp[i][j]

        if i == 0 or j == 0:
            dp[i][j] = max(i, j)
            return dp[i][j]

        if s1[i-1] == s2[j-1]:
            # current character match each other
            dp[i][j] = backtrack(i - 1, j - 1)
        else:
            # replace
            dp[i][j] = backtrack(i - 1, j - 1) + 1
            # add
            dp[i][j] = min(dp[i][j], backtrack(i, j - 1) + 1)
            # remove
            dp[i][j] = min(dp[i][j], backtrack(i - 1, j) + 1)

        return dp[i][j]

    return backtrack(sourceLen, targetLen)
