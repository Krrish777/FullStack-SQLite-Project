from typing import List, Optional, Any
from utils.logger import get_logger
logger = get_logger(__name__)

MAX_KEYS = 32  # Simulate a page size limit (adjust as needed)

class BTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf: bool = is_leaf
        self.keys: List[int] = []
        self.values: List[Any] = []            # Only for leaf nodes
        self.children: List['BTreeNode'] = []  # Only for internal nodes

    def is_full(self) -> bool:
        full = len(self.keys) >= MAX_KEYS
        logger.debug(f"Node {self} is_full({MAX_KEYS}) -> {full}")
        return full

    def __repr__(self):
        return f"<{'Leaf' if self.is_leaf else 'Internal'}Node keys={self.keys}>"

class BTree:
    def __init__(self):
        self.root = BTreeNode(is_leaf=True)
        logger.info(f"BTree initialized with MAX_KEYS={MAX_KEYS}")

    def search(self, key: int) -> Optional[Any]:
        logger.debug(f"Searching for key={key}")
        return self._search_in_node(self.root, key)

    def _search_in_node(self, node: BTreeNode, key: int) -> Optional[Any]:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            logger.debug(f"Key {key} found in node {node}")
            return node.values[i] if node.is_leaf else self._search_in_node(node.children[i + 1], key)

        if node.is_leaf:
            logger.debug(f"Key {key} not found in leaf node {node}")
            return None
        logger.debug(f"Descending to child {i} of node {node} in search for key {key}")
        return self._search_in_node(node.children[i], key)

    def insert(self, key: int, value: Any):
        logger.info(f"Inserting key={key}, value={value}")
        root = self.root
        if root.is_full():
            logger.debug("Root is full, splitting root")
            new_root = BTreeNode(is_leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
            logger.info("Root node split, new root created")
        self._insert_non_full(self.root, key, value)

    def _insert_non_full(self, node: BTreeNode, key: int, value: Any):
        if node.is_leaf:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if i < len(node.keys) and node.keys[i] == key:
                logger.debug(f"Updating existing key={key} in leaf node {node}")
                node.values[i] = value
                return
            logger.debug(f"Inserting key={key} at position {i} in leaf node {node}")
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            if node.children[i].is_full():
                logger.debug(f"Child {i} of node {node} is full, splitting child")
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            logger.debug(f"Descending to child {i} of node {node} for key={key}")
            self._insert_non_full(node.children[i], key, value)

    def _split_child(self, parent: BTreeNode, index: int):
        full = parent.children[index]
        mid = len(full.keys) // 2

        new_node = BTreeNode(is_leaf=full.is_leaf)

        if not full.is_leaf:
            new_node.keys = full.keys[mid + 1:]
            new_node.children = full.children[mid + 1:]
            promoted = full.keys[mid]
            full.keys = full.keys[:mid]
            full.children = full.children[:mid + 1]
            logger.info(f"Splitting internal node {full}, promoted key={promoted}")
        else:
            new_node.keys = full.keys[mid:]
            new_node.values = full.values[mid:]
            promoted = new_node.keys[0]
            full.keys = full.keys[:mid]
            full.values = full.values[:mid]
            logger.info(f"Splitting leaf node {full}, promoted key={promoted}")

        parent.keys.insert(index, promoted)
        parent.children.insert(index + 1, new_node)
        logger.debug(f"Parent after split: {parent}")

    def scan(self) -> List[tuple[int, Any]]:
        """
        Returns all key-value pairs in ascending order.
        """
        result = []
        logger.debug("Scanning all key-value pairs in BTree")

        def _scan(node: BTreeNode):
            if node.is_leaf:
                logger.debug(f"Scanning leaf node {node}")
                result.extend(zip(node.keys, node.values))
            else:
                for i in range(len(node.keys)):
                    _scan(node.children[i])
                _scan(node.children[-1])

        _scan(self.root)
        logger.info(f"Scan complete, {len(result)} items found")
        return result

    def print_tree(self):
        def _print(node: BTreeNode, level=0):
            indent = "  " * level
            print(f"{indent}{node}")
            if not node.is_leaf:
                for child in node.children:
                    _print(child, level + 1)
        logger.info("Printing BTree structure")
        _print(self.root)

    def load_from_file(self, pager, root_page):
        if root_page == 0:
            raise ValueError("Invalid root page 0")
        # ...existing code for loading from file...

# ------------------ Test ------------------

if __name__ == "__main__":
    bt = BTree()
    for k in range(1, 100):  # Insert more keys to test splits
        bt.insert(k, f"row{k}")

    print("Search:")
    print(bt.search(10))  # row10
    print(bt.search(99))  # row99

    print("\nTree structure:")
    bt.print_tree()

    print("\nIn-order scan:")
    for k, v in bt.scan():
        print(f"{k}: {v}")