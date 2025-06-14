import sys
sys.setrecursionlimit(50_000)

def naive_edit_distance(s1: str, s2: str) -> int:
    """
    Oblicza odległość edycyjną między dwoma ciągami używając naiwnego algorytmu rekurencyjnego.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Odległość edycyjna (minimalna liczba operacji wstawienia, usunięcia
        lub zamiany znaku potrzebnych do przekształcenia s1 w s2)
    """
    if len(s1) == 0:
        return len(s2)
    elif len(s2) == 0:
        return len(s1)
    elif s1[-1] == s2[-1]:
        return naive_edit_distance(s1[:-1], s2[:-1])

    return 1 + min(
        naive_edit_distance(s1, s2[:-1]),
        naive_edit_distance(s1[:-1], s2),
        naive_edit_distance(s1[:-1], s2[:-1])
    )

def naive_edit_distance_with_operations(s1: str, s2: str) -> tuple[int, list[str]]:
    """
    Oblicza odległość edycyjną i zwraca listę operacji potrzebnych do przekształcenia s1 w s2.

    Args:
        s1: Pierwszy ciąg znaków
        s2: Drugi ciąg znaków

    Returns:
        Krotka zawierająca odległość edycyjną i listę operacji
        Operacje: "INSERT x", "DELETE x", "REPLACE x->y", "MATCH x"
    """
    if len(s1) == 0:
        return len(s2), [f"INSERT {char}" for char in s2]
    elif len(s2) == 0:
        return len(s1), [f"DELETE {char}" for char in s1]
    elif s1[0] == s2[0]:
        dist, operations = naive_edit_distance_with_operations(s1[1:], s2[1:])
        return dist, operations + [f"MATCH {s1[0]}"]

    dist_delete, operations_delete = naive_edit_distance_with_operations(s1[1:], s2)
    dist_insert, operations_insert = naive_edit_distance_with_operations(s1, s2[1:])
    dist_replace, operations_replace = naive_edit_distance_with_operations(s1[1:], s2[1:])
    res_dist, res_operations = dist_delete, operations_delete + [f"DELETE {s1[0]}"]

    if dist_insert < res_dist:
        res_dist, res_operations = dist_insert, operations_insert + [f"INSERT {s2[0]}"]
    if dist_replace < res_dist:
        res_dist, res_operations = dist_replace, operations_replace + [f"REPLACE {s1[0]}->{s2[0]}"]

    return res_dist + 1, res_operations
