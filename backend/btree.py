from typing import List, Optional, Any

class BTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf: bool = is_leaf
        self.keys: List[int] = []
        self.values: List[Any] = []            # Only for leaf nodes
        self.children: List['BTreeNode'] = []  # Only for internal nodes

    def is_full(self, max_keys: int) -> bool:
        return len(self.keys) >= max_keys

    def __repr__(self):
        return f"<{'Leaf' if self.is_leaf else 'Internal'}Node keys={self.keys}>"

class BTree:
    def __init__(self, max_keys: int = 3):
        if max_keys < 1 or max_keys % 2 == 0:
            raise ValueError("max_keys must be an odd integer ≥ 1")
        self.max_keys = max_keys
        self.root = BTreeNode(is_leaf=True)

    def search(self, key: int) -> Optional[Any]:
        return self._search_in_node(self.root, key)

    def _search_in_node(self, node: BTreeNode, key: int) -> Optional[Any]:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i] if node.is_leaf else self._search_in_node(node.children[i + 1], key)

        if node.is_leaf:
            return None
        return self._search_in_node(node.children[i], key)

    def insert(self, key: int, value: Any):
        root = self.root
        if root.is_full(self.max_keys):
            new_root = BTreeNode(is_leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node: BTreeNode, key: int, value: Any):
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value
                return
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if node.children[i].is_full(self.max_keys):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent: BTreeNode, index: int):
        full = parent.children[index]
        mid = len(full.keys) // 2

        new_node = BTreeNode(is_leaf=full.is_leaf)

        # Internal node split
        if not full.is_leaf:
            new_node.keys = full.keys[mid + 1:]
            new_node.children = full.children[mid + 1:]
            promoted = full.keys[mid]
            full.keys = full.keys[:mid]
            full.children = full.children[:mid + 1]
        else:
            # Leaf split: mid stays in right and is promoted
            new_node.keys = full.keys[mid:]
            new_node.values = full.values[mid:]
            promoted = new_node.keys[0]
            full.keys = full.keys[:mid]
            full.values = full.values[:mid]

        parent.keys.insert(index, promoted)
        parent.children.insert(index + 1, new_node)

    def scan(self) -> List[tuple[int, Any]]:
        """
        Returns all key-value pairs in ascending order.
        """
        result = []

        def _scan(node: BTreeNode):
            if node.is_leaf:
                result.extend(zip(node.keys, node.values))
            else:
                for i in range(len(node.keys)):
                    _scan(node.children[i])
                _scan(node.children[-1])

        _scan(self.root)
        return result

    def print_tree(self):
        def _print(node: BTreeNode, level=0):
            indent = "  " * level
            print(f"{indent}{node}")
            if not node.is_leaf:
                for child in node.children:
                    _print(child, level + 1)
        _print(self.root)

# ------------------ Test ------------------

if __name__ == "__main__":
    bt = BTree(max_keys=3)
    for k in [5, 10, 15, 20, 25]:
        bt.insert(k, f"row{k}")

    print("Search:")
    print(bt.search(10))  # row10
    print(bt.search(25))  # row25

    print("\nTree structure:")
    bt.print_tree()

    print("\nIn-order scan:")
    for k, v in bt.scan():
        print(f"{k}: {v}")
