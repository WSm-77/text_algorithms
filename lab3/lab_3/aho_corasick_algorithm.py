from __future__ import annotations
from collections import deque
from typing import List, Tuple, Optional
from overrides import override

class AhoCorasickNode:
    def __init__(self, character: str, node_depth: int, is_terminal_node: bool = False):
        # Zainicjalizuj struktury potrzebne dla węzła w drzewie Aho-Corasick
        self.character: str = character
        self.goto_nodes: dict[str, AhoCorasickNode] = {}
        self.fail_link: Optional[AhoCorasickNode] = None
        self.output_link: Optional[AhoCorasickNode] = None
        self.node_depth: int = node_depth
        self.is_terminal_node: bool = is_terminal_node
        self.pattern: str = ""

    def get_character(self):
        return self.character

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

    def set_pattern(self, pattern: str):
        self.pattern = pattern

    def __repr__(self):
        return f'AhoCorasickNode(\'{self.character}\', {self.node_depth}, is_terminal={self.is_terminal_node}, ' + \
            f'fail=({None if self.fail_link is None else f"{self.fail_link.get_character()}, {self.fail_link.depth()}"}), ' + \
            f'output=({None if self.output_link is None else f"{self.output_link.get_character()}, {self.output_link.depth()}"}))'

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
            current_node.set_pattern(pattern)

    def _build_failure_links(self):
        """Builds failure links and propagates outputs through them."""
        # Zaimplementuj tworzenie failure links

        # Utwórz kolejkę do przechodzenia przez drzewo w szerokość (BFS)
        queue: deque[AhoCorasickNode] = deque([self.root])

        while queue:
            current_node = queue.popleft()

            # Użyj BFS do ustawienia łączy awaryjnych dla węzłów
            for char, goto_node in current_node.goto_nodes.items():
                queue.append(goto_node)

                # Zainicjalizuj łącza awaryjne dla węzłów na głębokości 1
                if current_node is self.root:
                    goto_node.set_fail(self.root)

                fail_node = current_node.fail()

                while fail_node is not None and fail_node is not self.root and fail_node.goto(char) is None:
                    fail_node = fail_node.fail()

                # sprawdzić czy ten if jest potrzebny; możliwe, że wystarczy zawsze
                # ustawiać tak jak w pierwszym casie
                if fail_node is not None and fail_node.goto(char) is not None:
                    goto_node.set_fail(fail_node.goto(char))
                else:
                    goto_node.set_fail(self.root)

            # Propaguj wyjścia przez łącza awaryjne
            output_node = current_node.fail()

            while output_node is not None and not output_node.is_terminal():
                output_node = output_node.fail()

            current_node.set_output(output_node)

    def search(self, text: str) -> List[Tuple[int, str]]:
        """
        Searches for all occurrences of patterns in the given text.

        Returns:
            List of tuples (start_index, pattern).
        """
        # Zaimplementuj wyszukiwanie wzorców w tekście

        result = []

        current_node: AhoCorasickNode = self.root

        for position, char in enumerate(text):
            while current_node.goto(char) is None:
                current_node = current_node.fail()

            current_node = current_node.goto(char)

            if current_node.is_terminal():
                result.append((position - current_node.depth() + 1, current_node.pattern))

            output_node = current_node.output()

            while output_node is not None:
                result.append((position - output_node.depth() + 1, output_node.pattern))
                output_node = output_node.output()

        # Zwróć listę krotek (indeks_początkowy, wzorzec)
        return result

    def __print_help(self, current_node: AhoCorasickNode, current_path: str, current_string: str):
        next_nodes = current_node.goto_nodes

        if not next_nodes:
            print(f"current string: {current_string}")
            print(f"current path: {current_path}")
            print()
            return

        for char, next_node in next_nodes.items():
            self.__print_help(next_node, f"{current_path} -> {next_node}\n", current_string + char)

    def print(self):
        self.__print_help(self.root, f"{self.root}\n", "")


if __name__ == "__main__":
    patterns = ["a", "na", "nam", "znana", "pozna"]
    text = "xpoznana"
    aho_corasick = AhoCorasick(patterns)
    aho_corasick.print()
    matches = aho_corasick.search(text)
    print(matches)
