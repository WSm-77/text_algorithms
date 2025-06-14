from enum import Enum, auto

class Operation(Enum):
    DELETE = auto()
    INSERT = auto()
    MATCH = auto()
    REPLACE = auto()
    LOCAL_0 = auto()


def make_key(source: str, target: str):
    return source + "$" + target

def allison_global_alignment(source: str, target: str,
                           match_score: int = 2,
                           mismatch_score: int = -1,
                           gap_penalty: int = -1) -> tuple[int, str, str]:
    """
    Znajduje optymalne globalne wyrównanie używając algorytmu Allisona.

    Args:
        source: Pierwszy ciąg znaków
        target: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania i dwa wyrównane ciągi
    """
    def dist(source: str, target: str):
        nonlocal hash_map, operations

        key = make_key(source, target)

        if key not in hash_map:
            if len(source) == 0:
                res = len(target) * gap_penalty
                operation = Operation.INSERT
            elif len(target) == 0:
                res = len(source) * gap_penalty
                operation = Operation.DELETE
            elif source[-1] == target[-1]:
                res = dist(source[:-1], target[:-1]) + match_score
                operation = Operation.MATCH
            else:
                res = max(
                    dist(source, target[:-1]) + gap_penalty,
                    dist(source[:-1], target) + gap_penalty,
                    dist(source[:-1], target[:-1]) + mismatch_score
                )

                if res == dist(source, target[:-1]) + gap_penalty:
                    operation = Operation.INSERT
                elif res == dist(source[:-1], target) + gap_penalty:
                    operation = Operation.DELETE
                else:
                    operation = Operation.REPLACE

            hash_map[key] = res
            operations[key] = operation

        return hash_map[key]

    hash_map = {}
    operations = {}

    res_dist = dist(source, target)

    source_alignment = ""
    target_alignment = ""

    source_idx = len(source)
    target_idx = len(target)
    while source_idx > 0 and target_idx > 0:
        key = make_key(source[:source_idx], target[:target_idx])
        operation = operations[key]
        if operation == Operation.MATCH or operation == Operation.REPLACE:
            source_alignment = source[source_idx - 1] + source_alignment
            target_alignment = target[target_idx - 1] + target_alignment
            source_idx -= 1
            target_idx -= 1
        elif operation == Operation.DELETE:
            source_alignment = source[source_idx - 1] + source_alignment
            target_alignment = "-" + target_alignment
            source_idx -= 1
        else: # Operation.INSERT
            source_alignment = "-" + source_alignment
            target_alignment = target[target_idx - 1] + target_alignment
            target_idx -= 1

    return res_dist,  source[:source_idx] + source_alignment, "-" * source_idx + target_alignment


def allison_local_alignment(source: str, target: str,
                          match_score: int = 2,
                          mismatch_score: int = -1,
                          gap_penalty: int = -1) -> tuple[int, str, str, int, int]:
    """
    Znajduje optymalne lokalne wyrównanie (podobnie do algorytmu Smith-Waterman).

    Args:
        source: Pierwszy ciąg znaków
        target: Drugi ciąg znaków
        match_score: Punkty za dopasowanie
        mismatch_score: Punkty za niedopasowanie
        gap_penalty: Kara za lukę

    Returns:
        Krotka zawierająca wynik wyrównania, dwa wyrównane ciągi oraz pozycje początku
    """
    def dist(source: str, target: str) -> int:
        nonlocal hash_map, operations, max_score, max_positions

        key = make_key(source, target)

        if key not in hash_map:
            if len(source) == 0:
                res = 0
                operation = Operation.INSERT
            elif len(target) == 0:
                res = 0
                operation = Operation.DELETE
            else:
                insert = dist(source, target[:-1]) + gap_penalty
                delete = dist(source[:-1], target) + gap_penalty
                match = dist(source[:-1], target[:-1]) + match_score if source[-1] == target[-1] else mismatch_score

                res = max(0, insert, delete, match)

                if res == insert:
                    operation = Operation.INSERT
                elif res == delete:
                    operation = Operation.DELETE
                else:
                    operation = Operation.MATCH if source[-1] == target[-1] else Operation.REPLACE

            if res == 0:
                operation = Operation.LOCAL_0

            if res > max_score:
                max_score = res
                max_positions = (len(source), len(target))

            hash_map[key] = res
            operations[key] = operation

        return hash_map[key]

    hash_map = {}
    operations = {}
    max_score = 0
    max_positions = (0, 0)

    dist(source, target)

    source_alignment = ""
    target_alignment = ""

    source_idx, target_idx = max_positions

    while source_idx > 0 and target_idx > 0 and hash_map[make_key(source[:source_idx], target[:target_idx])] != 0:
        key = make_key(source[:source_idx], target[:target_idx])
        operation = operations[key]
        if operation == Operation.MATCH or operation == Operation.REPLACE:
            source_alignment = source[source_idx - 1] + source_alignment
            target_alignment = target[target_idx - 1] + target_alignment
            source_idx -= 1
            target_idx -= 1
        elif operation == Operation.DELETE:
            source_alignment = source[source_idx - 1] + source_alignment
            target_alignment = "-" + target_alignment
            source_idx -= 1
        elif operation == Operation.INSERT:
            source_alignment = "-" + source_alignment
            target_alignment = target[target_idx - 1] + target_alignment
            target_idx -= 1
        else:
            break

    return max_score, source_alignment, target_alignment, source_idx, target_idx
