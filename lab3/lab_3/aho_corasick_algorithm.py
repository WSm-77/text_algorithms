from __future__ import annotations
from collections import deque
from typing import List, Tuple, Optional
from overrides import override

class AhoCorasickNode:
    pass

class AhoCorasickNode:
    def __init__(self, character: str, node_depth: int, is_terminal_node: bool = False):
        # Zainicjalizuj struktury potrzebne dla węzła w drzewie Aho-Corasick
        self.character: str = character
        self.goto_nodes: dict[str, AhoCorasickNode] = {}
        self.fail_link: Optional[AhoCorasickNode] = None
        self.output_link: Optional[AhoCorasickNode] = None
        self.node_depth: int = node_depth
        self.is_terminal_node: bool = is_terminal_node

    def goto(self, character: str) -> Optional[AhoCorasickNode]:
        return self.goto_nodes.get(character, None)

    def fail(self) -> Optional[AhoCorasickNode]:
        return self.fail_link

    def output(self) -> Optional[AhoCorasickNode]:
        return self.output_link

    def depth(self) -> int:
        return self.node_depth

    def is_terminal(self) -> bool:
        return self.is_terminal_node

    def add_goto(self, character: str, goto_node: AhoCorasickNode):
        assert character not in self.goto_nodes, f"goto node for character={character} already defined!!!"

        self.goto_nodes[character] = goto_node

    def set_fail(self, fail_node: Optional[AhoCorasickNode]):
        self.fail_link = fail_node

    def set_output(self, output_node: Optional[AhoCorasickNode]):
        self.output_link = output_node

    def set_is_terminal(self, is_terminal_node: bool):
        self.is_terminal_node = is_terminal_node

    def __repr__(self):
        return f'AhoCorasickNode(\'{self.character}\', {self.node_depth}, is_terminal={self.is_terminal_node})'

class AhoCorasickRootNode(AhoCorasickNode):
    def __init__(self):
        super().__init__('', 0, is_terminal_node = False)

    @override
    def goto(self, character: str) -> Optional[AhoCorasickNode]:
        if character not in self.goto_nodes:
            return self

        return super().goto(character)

class AhoCorasick:
    def __init__(self, patterns: List[str]):
        # Zainicjalizuj strukturę Aho-Corasick i usuń puste wzorce
        self.patterns = list(filter(lambda x: len(x) > 0, patterns))
        self.root: AhoCorasickNode = AhoCorasickRootNode()
        self._build_trie()
        self._build_failure_links()

    def _build_trie(self):
        """Builds the trie structure for the given patterns."""
        # Zaimplementuj budowanie drzewa typu trie dla podanych wzorców

        # Dodaj link do węzłów na pierwszym poziomie
        for pattern in self.patterns:
            char = pattern[0]

            if self.root.goto(char) == self.root:
                new_node = AhoCorasickNode(char, 1, is_terminal_node = len(pattern) == 1)
                self.root.add_goto(char, new_node)

        # Dodaj linki do pozostałych węzłów
        for pattern in self.patterns:
            current_node = self.root

            for depth, char in enumerate(pattern, start = 1):
                next_node = current_node.goto(char)

                if next_node is None:
                    next_node = AhoCorasickNode(char, depth)
                    current_node.add_goto(char, next_node)

                current_node = next_node

            current_node.set_is_terminal(True)

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        # TODO: Zaimplementuj tworzenie failure links
        # TODO: Utwórz kolejkę do przechodzenia przez drzewo w szerokość (BFS)
        # TODO: Zainicjalizuj łącza awaryjne dla węzłów na głębokości 1
        # TODO: Użyj BFS do ustawienia łączy awaryjnych dla głębszych węzłów
        # TODO: Propaguj wyjścia przez łącza awaryjne
        pass

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        # TODO: Zaimplementuj wyszukiwanie wzorców w tekście
        # TODO: Zwróć listę krotek (indeks_początkowy, wzorzec)
        return []

    def __print_help(self, current_node: AhoCorasickNode, current_path: str, current_string: str):
        next_nodes = current_node.goto_nodes

        if not next_nodes:
            print(f"current string: {current_string}")
            print(f"current path: {current_path}")
            return

        for char, next_node in next_nodes.items():
            self.__print_help(next_node, f"{current_path} -> {next_node}", current_string + char)

    def print(self):
        self.__print_help(self.root, "root", "")


if __name__ == "__main__":
    patterns = ["a", "na", "nam", "znana", "poznana"]
    aho_corasick = AhoCorasick(patterns)
    aho_corasick.print()
