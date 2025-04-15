def hamming_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość Hamminga między dwoma ciągami znaków.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość Hamminga (liczba pozycji, na których znaki się różnią)
        Jeśli ciągi mają różne długości, zwraca -1
    """
    # Zaimplementuj obliczanie odległości Hamminga
    if len(s1) != len(s2):
        return -1

    return sum(int(char1 != char2) for char1, char2 in zip(s1, s2))


def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
    # Zaimplementuj ustawianie n-tego bitu
    return 1 << n


def nth_bit(m: int, n: int) -> int:
    """
    Zwraca wartość n-tego bitu w masce m.

    Args:
        m: Maska bitowa
        n: Pozycja bitu do odczytania (0-indeksowana)

    Returns:
        Wartość n-tego bitu (0 lub 1)
    """
    # Zaimplementuj odczytywanie n-tego bitu
    return (m >> n) & 1


def make_mask(pattern: str) -> list:
    """
    Tworzy tablicę masek dla algorytmu Shift-Or.

    Args:
        pattern: Wzorzec do wyszukiwania

    Returns:
        Tablica 256 masek, gdzie każda maska odpowiada jednemu znakowi ASCII
    """
    # Zaimplementuj tworzenie tablicy masek dla algorytmu Shift-Or

    if len(pattern) == 0:
        return [0xff for _ in range(256)]

    # Utwórz tablicę z maskami dla wszystkich znaków ASCII
    masks = [2 ** len(pattern) - 1] * 256

    for n, character in enumerate(pattern):
        # Dla każdego znaku w pattern, ustaw odpowiednie bity w maskach
        masks[ord(character)] &= ~set_nth_bit(n)

    return masks


def fuzzy_shift_or(text: str, pattern: str, k: int = 2) -> list[int]:
    """
    Implementacja przybliżonego wyszukiwania wzorca przy użyciu algorytmu Shift-Or.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania
        k: Maksymalna dopuszczalna liczba różnic (odległość Hamminga)

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
        z maksymalnie k różnicami
    """
    # Zaimplementuj algorytm przybliżonego wyszukiwania Shift-Or

    # Obsłuż przypadki brzegowe (pusty wzorzec, wzorzec dłuższy niż tekst, k < 0)
    if len(pattern) == 0 or len(text) < len(pattern) or k < 0:
        return []

    result = []

    masks = make_mask(pattern)

    states = [2 ** len(pattern) - 1] * (k + 1)

    # Zaimplementuj główną logikę algorytmu
    for n, char in enumerate(text):
        state_idx = len(states) - 1
        while state_idx > 0:
            states[state_idx] = ((states[state_idx] << 1) | masks[ord(char)]) & (states[state_idx - 1] << 1)
            state_idx -= 1

        states[0] = (states[0] << 1) | masks[ord(char)]

        if nth_bit(states[-1], len(pattern) - 1) == 0:
            result.append(n - len(pattern) + 1)

    return result
