def set_nth_bit(n: int) -> int:
    """
    Zwraca maskę bitową z ustawionym n-tym bitem na 1.

    Args:
        n: Pozycja bitu do ustawienia (0-indeksowana)

    Returns:
        Maska bitowa z n-tym bitem ustawionym na 1
    """
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

def shift_or(text: str, pattern: str) -> list[int]:
    """
    Implementacja algorytmu Shift-Or do wyszukiwania wzorca.

    Args:
        text: Tekst do przeszukania
        pattern: Wzorzec do wyszukiwania

    Returns:
        Lista pozycji (0-indeksowanych), na których znaleziono wzorzec
    """
    # Zaimplementuj algorytm Shift-Or

    # Obsłuż przypadki brzegowe (pusty wzorzec, wzorzec dłuższy niż tekst)
    if len(pattern) == 0 or  len(text) < len(pattern):
        return []

    result = []

    # Utwórz maski dla wzorca
    masks = make_mask(pattern)

    # Zainicjalizuj stan początkowy
    state = 2 ** len(pattern) - 1

    # Zaimplementuj główną logikę algorytmu
    for n, char in enumerate(text):
        state = (state << 1) | masks[ord(char)]

        # Wykryj i zapisz pozycje dopasowań
        if nth_bit(state, len(pattern) - 1) == 0:
            result.append(n - len(pattern) + 1)

    return result
