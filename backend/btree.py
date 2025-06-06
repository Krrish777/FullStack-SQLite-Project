from typing import List, Optional, Any
class BTreeNode:
    def __init__(self, is_leaf: bool):
        self.is_leaf: bool = is_leaf
        self.keys: List[int] = []
        self.values: List[Any] = []
        self.children: List['BTreeNode'] = []
        
    def is_full(self, max_keys: int) -> bool:
        return len(self.keys) >= max_keys
    
    def __repr__(self):
        return f"<{'Leaf' if self.is_leaf else 'Internal'}Node keys={self.keys}>"
    
class BTree:
    def __init__(self, max_keys: int =3):
        self.root = BTreeNode(is_leaf=True)
        self.max_keys = max_keys
        
    def search(self, key: int) -> Optional[Any]:
        return self._search_in_node(self.root, key)
    
    def insert(self, key: int, value: any):
        pass
    
    def _search_in_node(self, node: BTreeNode, key:int) -> Optional[Any]:
        for i,k in enumerate(node.keys):
            if key == k:
                return node.values[i] if node.is_leaf else None
            elif key < k:
                if node.is_leaf:
                    return None
                return self._search_in_node(node.children[i], key)
        if node.is_leaf:
            return None
        return self._search_in_node(node.children[i], key)
        
btree = BTree()
btree.root.keys = [10, 20]
btree.root.values = ["row10", "row20"]  # Because it’s a leaf

print(btree.search(10))  # → row10
print(btree.search(15))  # → None
