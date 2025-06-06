from typing import List, Optional, Any

class BTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf: bool = is_leaf
        self.keys: List[int] = []
        self.values: List[Any] = []  # Only used in leaf nodes
        self.children: List['BTreeNode'] = []  # Only used in internal nodes

    def is_full(self, max_keys: int) -> bool:
        return len(self.keys) >= max_keys

    def __repr__(self):
        return f"<{'Leaf' if self.is_leaf else 'Internal'}Node keys={self.keys}>"


class BTree:
    def __init__(self, max_keys: int = 3):
        self.root = BTreeNode(is_leaf=True)
        self.max_keys = max_keys

    def search(self, key: int) -> Optional[Any]:
        return self._search_in_node(self.root, key)

    def _search_in_node(self, node: BTreeNode, key: int) -> Optional[Any]:
        for i, k in enumerate(node.keys):
            if key == k:
                if node.is_leaf:
                    return node.values[i]
                else:
                    return self._search_in_node(node.children[i + 1], key)
            elif key < k:
                if node.is_leaf:
                    return None
                return self._search_in_node(node.children[i], key)

        if node.is_leaf:
            return None
        return self._search_in_node(node.children[-1], key)

    def insert(self, key: int, value: Any):
        root = self.root
        if root.is_full(self.max_keys):
            promoted_key, right_node = self._split_leaf(root)

            new_root = BTreeNode(is_leaf=False)
            new_root.keys.append(promoted_key)
            new_root.children.append(root)
            new_root.children.append(right_node)
            self.root = new_root

        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node: BTreeNode, key: int, value: Any):
        if node.is_leaf:
            self._insert_into_leaf(node, key, value)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            child = node.children[i]

            if child.is_full(self.max_keys):
                if child.is_leaf:
                    promoted_key, right_node = self._split_leaf(child)
                else:
                    raise NotImplementedError("Splitting internal nodes not implemented.")

                node.keys.insert(i, promoted_key)
                node.children.insert(i + 1, right_node)

                if key > promoted_key:
                    child = right_node

            self._insert_non_full(child, key, value)

    def _insert_into_leaf(self, node: BTreeNode, key: int, value: Any):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            node.values[i] = value
            return

        node.keys.insert(i, key)
        node.values.insert(i, value)

    def _split_leaf(self, node: BTreeNode) -> (int, BTreeNode):
        mid = len(node.keys) // 2

        right_node = BTreeNode(is_leaf=True)
        right_node.keys = node.keys[mid:]
        right_node.values = node.values[mid:]

        node.keys = node.keys[:mid]
        node.values = node.values[:mid]

        promoted_key = right_node.keys[0]
        return promoted_key, right_node


# ------------------------ Test Code ------------------------

if __name__ == "__main__":
    bt = BTree(max_keys=3)

    for k in [5, 10, 15, 20, 25]:
        bt.insert(k, f"row{k}")

    print(bt.search(10))   # Should print: row10
    print(bt.search(25))   # Should print: row25

    print(bt.root)               # <InternalNode keys=[15]>
    print(bt.root.children[0])  # <LeafNode keys=[5, 10]>
    print(bt.root.children[1])  # <LeafNode keys=[15, 20, 25]>
