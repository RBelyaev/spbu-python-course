import random
from typing import Optional, Iterator, Tuple, Any
from collections.abc import MutableMapping


class TreapNode:
    def __init__(self, key: int, value: Any, priority: Optional[int] = None) -> None:
        """
        Node of the Treap data structure.

        Attributes:
        key (int): The key of the node.
        value (Any): The value associated with the key.
        priority (int): Node priority (random default value).
        left (Optional[TreapNode]): The left child node.
        right (Optional[TreapNode]): The right child node.

        Args:
        key (int): The key of the node.
        value (Any): The value of the node.
        priority (Optional[int]): The optional priority of the node.

        Returns:
        There is no return value.

        Raises:
        There are no exceptions.
        """
        self.key: int = key
        self.value: Any = value
        self.priority: int = (
            priority if priority is not None else random.randint(1, 2**31 - 1)
        )
        self.left: Optional[TreapNode] = None
        self.right: Optional[TreapNode] = None


class Treap(MutableMapping):
    """
    Implementation of a Treap (tree + heap) data structure that supports the MutableMapping interface.

    Treap combines the properties of a binary search tree and a heap, providing efficient insertion, deletion, and search operations.
    """

    def __init__(self, root: Optional[TreapNode] = None) -> None:
        """
        Args:
        root (Optional[TreapNode]): The root node of the Treap (None by default).

        Returns:
        There is no return value (constructor).

        Raises:
        There are no exceptions.
        """
        self.root: Optional[TreapNode] = root

    def split(
        self, node: Optional[TreapNode], key: int
    ) -> Tuple[Optional[TreapNode], Optional[TreapNode]]:
        """
        Splits a Treap into two subtrees by a given key.

        Args:
        node (Optional[TreapNode]): The root node for separation.
        key (int): The key to split.

        Returns:
        Tuple[Optional[TreapNode], Optional[TreapNode]]: Two subtrees (keys < key and keys>= key).

        Raises:
        There are no exceptions.
        """
        if node is None:
            return None, None
        elif key < node.key:
            left, node.left = self.split(node.left, key)
            return left, node
        else:
            node.right, right = self.split(node.right, key)
            return node, right

    def merge(
        self, left_node: Optional[TreapNode], right_node: Optional[TreapNode]
    ) -> Optional[TreapNode]:
        """
        Combines two Treaps into one while preserving the properties of the structure.

        Args:
        left_node (Optional[TreapNode]): The root of the left subtree.
        right_node (Optional[TreapNode]): The root of the right subtree.

        Returns:
        Optional[TreapNode]: The root of the combined tree.

        Raises:
        There are no exceptions.
        """
        if right_node is None:
            return left_node
        if left_node is None:
            return right_node
        elif left_node.priority > right_node.priority:
            left_node.right = self.merge(left_node.right, right_node)
            return left_node
        else:
            right_node.left = self.merge(left_node, right_node.left)
            return right_node

    def insert(self, node: Optional[TreapNode], key: int, value: Any) -> TreapNode:
        """
        Inserts a new node or updates the value of an existing one.

        Args:
        node (Ttreenode): The root node.
        key (int): The key to insert.
        value (Any): The value to insert.

        Returns:
        TreapNode: The root of the tree after insertion.

        Raises:
        There are no exceptions.
        """
        new_node = self.get_node(key)
        if new_node is not None:
            new_node.value = value
            return self.root

        new_node = TreapNode(key, value)
        node_1, node_2 = self.split(node, key)
        return self.merge(self.merge(node_1, new_node), node_2)

    def __len__(self) -> int:
        """
        Returns the node by key.

        Args:
        key (int): The key to search for.

        Returns:
        TreapNode: Found node or None.

        Raises:
        There are no exceptions.
        """
        return sum(1 for _ in self)

    def __contains__(self, key: Any) -> bool:
        """
        Iterator for traversing Treap in ascending order of keys.

        Args:
        node (Optional[TreapNode]): The root node to crawl.

        Yields:
        Iterator: The keys of the tree are in ascending order.

        Raises:
        There are no exceptions.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __setitem__(self, key: int, value: Any) -> None:
        """
        Iterator for traversing Treap in descending order of keys.

        Args:
        node (Optional[TreapNode]): The root node to crawl.

        Yields:
        Iterator: The keys of the tree are in descending order.

        Raises:
        There are no exceptions.
        """
        self.root = self.insert(self.root, key, value)

    def get_node(self, key: int) -> Optional[TreapNode]:
        """
        Searching for a node in a Treap using a given key.

        Args:
        key (int): The key to search in the tree.

        Returns:
        TreapNode: Found node or None if a node with such a key does not exist.

        Raises:
        There are no exceptions.
        """
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return node

    def __getitem__(self, key: int) -> str:
        """
        Returns the value by key.

        Args:
        key (int): The key to search for.

        Returns:
        str: The value associated with the key.

        Raises:
        KeyError: If the key is not found.
        """
        node = self.get_node(key)
        if node == None:
            raise KeyError(f"Key {key} not found.")
        return node.value

    def __delitem__(self, key: int) -> None:
        """
        Deletes the node with the specified key.

        Args:
        key (int): The key to delete.

        Returns:
        There is no return value.

        Raises:
        KeyError: If the key is not found.
        """
        parent = None
        node = self.root

        while node and node.key != key:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is None:
            raise KeyError(f"Key {key} not found")

        new_child = self.merge(node.left, node.right)

        if parent is None:
            self.root = new_child
        elif parent.left == node:
            parent.left = new_child
        else:
            parent.right = new_child

    def __iter__(self) -> Iterator:
        """
        Returns an iterator for traversing keys in ascending order.

        Args:
        There are no arguments.

        Returns:
        Iterator: Key iterator.

        Raises:
        There are no exceptions.
        """
        return self.inorder_iter(self.root)

    def inorder_iter(self, node: Optional[TreapNode]) -> Iterator:
        """
        Auxiliary method for inorder traversal (ascending).

        Args:
        node (Optional[TreapNode]): The node to start the crawl.

        Yields:
        Iterator: Keys in ascending order.

        Raises:
        There are no exceptions.
        """
        if node:
            yield from self.inorder_iter(node.left)
            yield node.key
            yield from self.inorder_iter(node.right)

    def __reversed__(self) -> Iterator:
        """
        Returns an iterator for traversing keys in descending order.

        Args:
        There are no arguments.

        Returns:
        Iterator: Key iterator.

        Raises:
        There are no exceptions.
        """
        return self.reverse_inorder_iter(self.root)

    def reverse_inorder_iter(self, node: Optional[TreapNode]) -> Iterator:
        """
        Auxiliary method for reverse inorder traversal (descending).

        Args:
        node (Optional[TreapNode]): The node to start the crawl.

        Yields:
        Iterator: Keys in descending order.

        Raises:
        There are no exceptions.
        """
        if node:
            yield from self.reverse_inorder_iter(node.right)
            yield node.key
            yield from self.reverse_inorder_iter(node.left)

    def __repr__(self) -> str:
        """
        Returns the string representation of the Treap.

        Returns
        -------
        str
            The string representation of the Treap.
        """
        return f"Treap({list(self)})"
