def wagner_fischer(source: str, target: str,
                  insert_cost: int = 1,
                  delete_cost: int = 1,
                  substitute_cost: int = 1) -> int:
    """
    Oblicza odległość edycyjną używając algorytmu Wagnera-Fischera (programowanie dynamiczne).

    Args:
        source: Pierwszy ciąg znaków
        target: Drugi ciąg znaków
        insert_cost: Koszt operacji wstawienia
        delete_cost: Koszt operacji usunięcia
        substitute_cost: Koszt operacji zamiany

    Returns:
        Odległość edycyjna z uwzględnieniem kosztów operacji
    """
    source_len = len(source)
    target_len = len(target)
    dp = [[0 for _ in range(target_len + 1)] for _ in range(source_len + 1)]

    for row in range(1, source_len + 1):
        dp[row][0] = row

    for col in range(1, target_len + 1):
        dp[0][col] = col

    for row in range(1, source_len + 1):
        for col in range(1, target_len + 1):
            if source[row - 1] == target[col - 1]:
                dp[row][col] = dp[row - 1][col - 1]
            else:
                dp[row][col] = min(dp[row][col - 1] + insert_cost, dp[row - 1][col] + delete_cost, dp[row - 1][col - 1] + substitute_cost)

    return dp[-1][-1]

def wagner_fischer_with_alignment(source: str, target: str) -> tuple[int, str, str]:
    """
    Oblicza odległość edycyjną i zwraca wyrównanie sekwencji.

    Args:
        source: Pierwszy ciąg znaków
        target: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i dwa wyrównane ciągi
        (w wyrównanych ciągach '-' oznacza lukę)
    """
    source_len = len(source)
    target_len = len(target)

    # Inicjalizacja macierzy DP i macierzy operacji
    dp = [[0 for _ in range(target_len + 1)] for _ in range(source_len + 1)]
    operations = [['' for _ in range(target_len + 1)] for _ in range(source_len + 1)]

    # Inicjalizacja pierwszego wiersza i kolumny
    for row in range(1, source_len + 1):
        dp[row][0] = row
        operations[row][0] = 'D'  # Delete

    for col in range(1, target_len + 1):
        dp[0][col] = col
        operations[0][col] = 'I'  # Insert

    for row in range(1, source_len + 1):
        for col in range(1, target_len + 1):
            if source[row - 1] == target[col - 1]:
                dp[row][col] = dp[row - 1][col - 1]
                operations[row][col] = 'M'
            else:
                insert = dp[row][col - 1] + 1
                delete = dp[row - 1][col] + 1
                substitute = dp[row - 1][col - 1] + 1

                dp[row][col] = min(insert, delete, substitute)

                if dp[row][col] == insert:
                    operations[row][col] = 'I'
                elif dp[row][col] == delete:
                    operations[row][col] = 'D'
                else:
                    operations[row][col] = 'S'

    aligned_source = ""
    aligned_target = ""
    row, col = source_len, target_len

    while row > 0 or col > 0:
        if row == 0:
            aligned_source = '-' +  aligned_source
            aligned_target = target[col - 1] + aligned_target
            col -= 1
        elif col == 0:
            aligned_source = source[row - 1] + aligned_source
            aligned_target = '-' + aligned_target
            row -= 1
        else:
            op = operations[row][col]
            if op == 'M':
                aligned_source = source[row - 1] + aligned_source
                aligned_target = target[col - 1] + aligned_target
                row -= 1
                col -= 1
            elif op == 'S':
                aligned_source = source[row - 1] + aligned_source
                aligned_target = target[col - 1] + aligned_target
                row -= 1
                col -= 1
            elif op == 'D':
                aligned_source = source[row - 1] + aligned_source
                aligned_target = '-' + aligned_target
                row -= 1
            else:  # op == 'I'
                aligned_source = '-' + aligned_source
                aligned_target = target[col - 1] + aligned_target
                col -= 1

    return dp[-1][-1], aligned_source, aligned_target

def wagner_fischer_space_optimized(source: str, target: str) -> int:
    """
    Oblicza odległość edycyjną używając zoptymalizowanej pamięciowo wersji algorytmu.

    Args:
        source: Pierwszy ciąg znaków
        target: Drugi ciąg znaków

    Returns:
        Odległość edycyjna
    """
    source_len = len(source)
    target_len = len(target)

    if target_len < source_len:
        source, target = target, source
        source_len, target_len = target_len, source_len

    dp1 = [row for row in range(source_len + 1)]
    dp2 = [row for row in range(source_len + 1)]

    for col in range(1, target_len + 1):
        dp2[0] = col
        for row in range(1, source_len + 1):
            if source[row - 1] == target[col - 1]:
                dp2[row] = dp1[row - 1]
            else:
                dp2[row] = 1 + min(dp2[row - 1], dp1[row], dp1[row - 1])
        dp1, dp2 = dp2, dp1

    return dp1[-1]
