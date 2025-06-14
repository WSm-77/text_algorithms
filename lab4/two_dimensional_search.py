from lab4.shift_or_algorithm import shift_or

def find_pattern_in_column(text_column: str, pattern_columns: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wszystkie kolumny wzorca w kolumnie tekstu.

    Args:
        text_column: Kolumna tekstu
        pattern_columns: Lista kolumn wzorca

    Returns:
        Lista krotek (pozycja, indeks kolumny), gdzie znaleziono kolumnę wzorca
    """
    # Zaimplementuj wyszukiwanie kolumn wzorca w kolumnie tekstu
    result = []

    for collumn_idx, pattern in enumerate(pattern_columns):
        # Dla każdej kolumny wzorca, przeszukaj kolumnę tekstu
        matches = shift_or(text_column, pattern)
        matches = list(map(lambda x: (x, collumn_idx), matches))
        result.extend(matches)

    # Zwróć listę krotek (pozycja, indeks kolumny) dla znalezionych dopasowań
    return result


def find_pattern_2d(text: list[str], pattern: list[str]) -> list[tuple[int, int]]:
    """
    Wyszukuje wzorzec dwuwymiarowy w tekście dwuwymiarowym.

    Args:
        text: Tekst dwuwymiarowy (lista ciągów znaków tej samej długości)
        pattern: Wzorzec dwuwymiarowy (lista ciągów znaków tej samej długości)

    Returns:
        Lista krotek (i, j), gdzie (i, j) to współrzędne lewego górnego rogu wzorca w tekście
    """
    # Zaimplementuj wyszukiwanie wzorca dwuwymiarowego

    # Obsłuż przypadki brzegowe (pusty tekst/wzorzec, wymiary)
    # Sprawdź, czy wszystkie wiersze mają taką samą długość
    if len(pattern) == 0 or \
        len(pattern[0]) == 0 or \
        len(text) < len(pattern) or \
        len(text[0]) < len(pattern[0]) or \
        any(len(text_line) != len(text[0]) for text_line in text) or \
        any(len(pattern_line) != len(pattern[0]) for pattern_line in pattern):

        return []

    text_columns = [''.join(column) for column in zip(*text)]
    pattern_columns_matches: dict[tuple[int, int], set] = {}
    pattern_columns = [''.join(column) for column in zip(*pattern)]

    # Zaimplementuj algorytm wyszukiwania dwuwymiarowego
    for column_idx, text_column in enumerate(text_columns):
        pattern_in_column = find_pattern_in_column(text_column, pattern_columns)

        for row, pattern_column_idx in pattern_in_column:
            key = (row, column_idx)
            pattern_match_set = pattern_columns_matches.get(key, set())
            pattern_match_set.add(pattern_column_idx)
            pattern_columns_matches[key] = pattern_match_set

    result = []

    for row in range(len(text)):

        for col_start in range(len(text_columns) - len(pattern_columns) + 1):
            key = (row, col_start)
            # Sprawdź czy w pierwszej kolumnie znaleziono pattern
            pattern_detected = key in pattern_columns_matches and 0 in pattern_columns_matches[key]

            if not pattern_detected:
                continue

            # Sprawdź czy kolejne kolumny tworzą spójny ciąg rosnący
            for pattern_col_idx in range(1, len(pattern_columns)):
                col = col_start + pattern_col_idx
                key = (row, col)

                # Sprawdź czy została zachowana kolejność kolumn w ciągu
                if key not in pattern_columns_matches or pattern_col_idx not in pattern_columns_matches[key]:
                    pattern_detected = False
                    break

            # Dodaj pozycję wzorca do rezultatu, jeżeli został on wykryty
            if pattern_detected:
                result.append((row, col_start))

    # Zwróć listę współrzędnych lewego górnego rogu dopasowanego wzorca
    return result
