from __future__ import annotations
from typing import Optional
from collections import deque

class IntRef:
    def __init__(self, value):
        self.value = value

class Node:
    text: str = ""
    def __init__(self, end: IntRef, start: int = -1, id: int = -1, suffix_link: Optional[Node] = None):
        self.children: dict[str, Node] = {}
        self.suffix_link: Optional[Node] = suffix_link
        self.start: int = start
        self.end: IntRef = end
        self.id: int = id

    def width(self):
        return self.end.value - self.start + 1

    def debug_str(self):
        return f"Node(\"{self.text[self.start:self.end.value + 1]}\", start: {self.start}, end: {self.end.value} id: {self.id}, link: {self.suffix_link})"

    def __repr__(self):
        return f"Node(\"{self.text[self.start:self.end.value + 1]}\")"

class SuffixTree:
    def __init__(self, text: str):
        """
        Construct a suffix tree for the given text using Ukkonen's algorithm.

        Args:
            text: The input text for which to build the suffix tree
        """
        self.guardian: str = "$"
        self.end_ref: IntRef = IntRef(0)
        self.text: str = text + self.guardian
        self.root: Node = Node(IntRef(-1), start=0)
        self.active_node: Node = self.root
        self.active_edge: int = 0
        self.active_length: int = 0
        self.remainder: int = 0
        self.leaf_id: int = 0

        Node.text = self.text

        self.build_tree()

    def build_tree(self):
        """
        Build the suffix tree using Ukkonen's algorithm.
        """
        text_len = len(self.text)
        self.remainder = 0

        for i in range(text_len):
            self.extend_tree(i)

    def get_node_first_char(self, node: Node):
        return self.text[node.start]

    def add_child_node(self, parent: Node, child: Node):
        parent.children[self.get_node_first_char(child)] = child

    def get_current_child(self):
        return self.active_node.children[self.get_active_edge_char()]

    def get_active_edge_char(self):
        return self.text[self.active_edge]

    def create_leaf(self, start: int):
        leaf = Node(end = self.end_ref, start = start, id = self.leaf_id)
        self.leaf_id += 1

        return leaf

    def extend_tree(self, position):
        self.end_ref.value = position
        curr_char = self.text[position]
        last_added_node: Optional[Node] = None
        self.remainder += 1

        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = position

            if self.get_active_edge_char() not in self.active_node.children:
                new_leaf = self.create_leaf(position)
                self.add_child_node(self.active_node, new_leaf)

                if last_added_node is not None:
                    last_added_node.suffix_link = self.active_node
                    last_added_node = None
            else:
                curr_child = self.get_current_child()
                idx = curr_child.start + self.active_length

                # update current node if exceeding it's length
                if curr_child.width() <= self.active_length:
                    self.active_node = curr_child
                    self.active_length -= curr_child.width()
                    self.active_edge += curr_child.width()
                    continue

                # check if we don't have to devide current active_edge
                if self.text[idx] == curr_char:
                    if last_added_node is not None:
                        last_added_node.suffix_link = self.active_node
                    self.active_length += 1
                    break

                inner_node_end_ref = IntRef(curr_child.start + self.active_length - 1)
                inner_node = Node(end = inner_node_end_ref, start = curr_child.start)
                self.add_child_node(self.active_node, inner_node)

                if last_added_node is not None:
                    last_added_node.suffix_link = inner_node

                curr_child.start = inner_node.end.value + 1
                new_leaf = self.create_leaf(position)

                self.add_child_node(inner_node, curr_child)
                self.add_child_node(inner_node, new_leaf)

                last_added_node = inner_node

                if self.active_node is self.root:
                    self.active_length -= 1
                    self.active_edge += 1

            self.remainder -= 1
            if self.active_node is not self.root:
                if self.active_node.suffix_link is not None:
                    self.active_node = self.active_node.suffix_link
                else:
                    self.active_node = self.root

    def find_pattern(self, pattern: str) -> list[int]:
        """
        Find all occurrences of the pattern in the text.

        Args:
            pattern: The pattern to search for

        Returns:
            A list of positions where the pattern occurs in the text
        """

        if len(pattern) == 0 or pattern[0] not in self.root.children:
            return []

        curr_node = self.root.children[pattern[0]]
        pattern_found = True

        pos = 0

        for i in range(1, len(pattern)):
            char = pattern[i]
            pos += 1
            if pos < curr_node.width():
                if char != self.text[curr_node.start + pos]:
                    pattern_found = False
                    break
            else:
                if char in curr_node.children:
                    curr_node = curr_node.children[char]
                    pos = 0
                else:
                    pattern_found = False
                    break

        if not pattern_found:
            return []

        result = []
        to_check = deque([curr_node])

        while to_check:
            node = to_check.popleft()

            if not node.children:
                result.append(node.id)
                continue

            for child_node in node.children.values():
                to_check.append(child_node)

        return result

    def __print_help(self, current_node: Node, current_path: str, current_string: str):
        next_nodes = current_node.children

        if not next_nodes:
            print(f"current string: {current_string + self.text[current_node.start:current_node.end.value + 1]}")
            print(f"current path: {current_path}")
            print()
            return

        for next_node in next_nodes.values():
            self.__print_help(next_node, f"{current_path} -> {next_node.debug_str()}\n", current_string + self.text[current_node.start:current_node.end.value + 1])

    def print(self):
        self.__print_help(self.root, f"{self.root.debug_str()}\n", "")

    def count_suffixes(self):
        def count_suffixes_help(current_node: Node):
            nonlocal cnt
            next_nodes = current_node.children

            if not next_nodes:
                cnt += 1
                return

            for next_node in next_nodes.values():
                count_suffixes_help(next_node)
        cnt = 0
        count_suffixes_help(self.root)

        return cnt

    def contains_suffix(self, suffix: str):
        if suffix[0] not in self.root.children:
            return False

        curr_node = self.root.children[suffix[0]]
        pos = 0

        for char in suffix[1:]:
            pos += 1
            if pos < curr_node.width():
                if char != self.text[curr_node.start + pos]:
                    return False
            else:
                if char in curr_node.children:
                    curr_node = curr_node.children[char]
                    pos = 0
                else:
                    return False

        return True

if __name__ == "__main__":
    text = "ananas"
    trie = SuffixTree(text)
    trie.print()
    pattern = "ana"
    pattern_idx = trie.find_pattern(pattern)
    print("text:")
    print(text)
    print()
    print(f"pattern '{pattern}' found at {pattern_idx}")
