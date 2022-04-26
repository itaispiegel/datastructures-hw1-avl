# username - itaispiegel
# id1      - 206781569
# name1    - Itai Spiegel
# id2      - 322573007
# name2    - Oren Shacham


class AVLNode(object):
    """A class representing a node in an AVL tree"""

    def __init__(self, value=None, parent=None):
        """
        Constructor, you are allowed to add more fields.

        @type value: Optional[str]
        @param value: Optional data for the node. If None, then the node will be considered virtual.
        @type parent: AVLNode
        @param parent: The parent node to set.
        """
        self.value = value
        self.parent = parent

        if value is None:
            self.left = None
            self.right = None
            self.height = -1
            self.rank = 0
        else:
            self.left = AVLNode(parent=self)
            self.right = AVLNode(parent=self)
            self.rank = 1
            self.height = 0

    def getPredecessor(self):
        """
        Returns the predecessor node.
        Go down left and then all the way down right if there's a left son, otherwise go all the way up right.
        Complexity: O(log(n)) worst case and O(1) amortized.

        @rtype: AVLNode
        @returns: The node with index-1, or None if none exist (first item).
        """
        node = self
        if node.left.isRealNode():
            node = node.left
            while node.right.isRealNode():
                node = node.right
            return node
        else:
            while node.parent is not None and node.isParentRight():
                node = node.parent
            return node.parent

    def getSuccessor(self):
        """
        Returns the successor node.
        Go down right and then all the way down left if there's a right son, otherwise go all the way up left.
        Complexity: O(log(n)) worst case and O(1) amortized.

        @rtype: AVLNode
        @return: The node with the index+1, or None if none exist (last item).
        """
        node = self
        if node.right.isRealNode():
            node = node.right
            while node.left.isRealNode():
                node = node.left
            return node
        else:
            while node.parent is not None and not node.isParentRight():
                node = node.parent
            return node.parent

    def getLeft(self):
        """
        Returns the left child.
        Complexity: O(1).

        @rtype: AVLNode
        @returns: The left child of self, None if there is no left child
        """
        if self.isRealNode():
            return self.left
        return None

    def getRight(self):
        """
        Returns the right child.
        Complexity: O(1).

        @rtype: AVLNode
        @returns: The right child of self, None if there is no right child
        """
        if self.isRealNode():
            return self.right
        return None

    def getParent(self):
        """
        Returns the parent.
        Complexity: O(1).

        @rtype: AVLNode
        @returns: The parent of self, None if there is no parent
        """
        return self.parent

    def getValue(self):
        """
        Return the value.
        Complexity: O(1).

        @rtype: str
        @returns: The value of self, None if the node is virtual
        """
        return self.value

    def getHeight(self):
        """
        Returns the height.
        Complexity: O(1).

        @rtype: int
        @returns: The height of self, -1 if the node is virtual
        """
        return self.height

    def setLeft(self, node):
        """
        Sets left child.
        Complexity: O(1).

        @type node: AVLNode
        @param node: a node
        """
        self.left = node
        node.setParent(self)

    def setRight(self, node):
        """
        Sets right child.
        Complexity: O(1).

        @type node: AVLNode
        @param node: a node
        """
        self.right = node
        node.setParent(self)

    def setParent(self, node):
        """
        Sets parent.
        Complexity: O(1).

        @type node: AVLNode
        @param node: a node
        """
        self.parent = node

    def setValue(self, value):
        """
        Sets value.
        Complexity: O(1).

        @type value: str
        @param value: data
        """
        self.value = value

    def setHeight(self, h):
        """
        Sets the height of the node.
        Complexity: O(1).

        @type h: int
        @param h: the height
        """
        self.height = h

    def isRealNode(self):
        """
        Returns whether self is a real node.
        Complexity: O(1).

        @rtype: bool
        @returns: True iff self is a real node.
        """
        return self.height != -1

    def isVirtualNode(self):
        """
        Returns whether self is a virtual node.
        Complexity: O(1).

        @rtype: bool
        @returns: True iff self is a virtual node.
        """
        return not self.isRealNode()

    def update(self):
        """
        Update the node's fields from its children.
        Complexity: O(1).

        @rtype: node
        @returns: None
        """
        self.rank = self.left.rank + 1 + self.right.rank
        new_height = max(self.left.height, self.right.height) + 1
        updates = int(self.height != new_height)
        self.height = new_height
        return updates

    def isParentRight(self):
        """
        Checks if the given node's parent is to its left or right.
        Complexity: O(1).

        @rtype: bool
        @returns: True iff the node's parent is to the right of it.
        """
        return self.parent is not None and self.parent.left == self

    def isLeafNode(self):
        """
        Returns whether the current node is a leaf.
        Note that a node will be considered a leaf iff both of its children are virtual nodes.
        Complexity: O(1).

        @rtype: bool
        """
        return self.left.isVirtualNode() and self.right.isVirtualNode()

    def depth(self):
        """
        Returns the depth of the current node, by going all the way up to the root and counting the nodes in the path.
        Complexity: O(log(n)).

        @rtype: int
        """
        count, node = 0, self
        while node.parent is not None:
            count += 1
            node = node.parent
        return count

    @property
    def balanceFactor(self):
        """
        Returns the balance factor of the given node, which is the difference in height of the left node and the right.
        Complexity: O(1).

        @rtype: int
        @returns: The node's balance factor.
        """
        left_height = getattr(self.left, "height", 0)
        right_height = getattr(self.right, "height", 0)
        return left_height - right_height


class AVLTreeList(object):
    """
    A class implementing the ADT list, using an AVL tree.
    """

    def __init__(self, root=None, remove_parent_from_root=False):
        """
        Constructor, you are allowed to add more fields.

        @type root: AVLNode
        @param root: The root of this new tree list.
        @type remove_parent_from_root: bool
        @param remove_parent_from_root: Whether to set the parent of the root as None. Setting this flag to True might
        have side effects on the passed node.
        """
        self.root = root or AVLNode()
        if remove_parent_from_root:
            self.root.parent = None
        self.first_node = self.last_node = self.root

    def empty(self):
        """
        Returns whether the list is empty.
        Complexity: O(1).

        @rtype: bool
        @returns: True if the list is empty, False otherwise
        """
        return self.root.isVirtualNode()

    def retrieve(self, index):
        """
        Retrieves the value of the ith item in the list.
        Complexity: O(log(n)).

        @type index: int
        @pre: 0 <= index < self.length()
        @param index: index in the list
        @rtype: str
        @returns: The value of the ith item in the list
        """
        if index >= self.root.rank:
            return None

        node = self.get(index + 1)
        return node.value

    def insert(self, index, val):
        """
        Inserts val at position i in the list.
        Complexity: O(log(n)).

        @type index: int
        @pre: 0 <= index <= self.length()
        @param index: The intended index in the list to which we insert val
        @type val: str
        @param val: the inserted value
        @rtype: int
        @returns: The number of re-balance operation due to AVL re-balancing.
        """
        fixes = 0
        if index > self.length():
            return fixes
        elif self.empty() and index == 0:
            self.root = AVLNode(val)
            self.first_node = self.last_node = self.root
        elif index <= self.length() - 1:
            node = self.get(index + 1)
            if node.left.isVirtualNode():
                child = AVLNode(val, node)
                node.left = child
            else:
                pred = node.getPredecessor()
                child = AVLNode(val, pred)
                pred.right = child
            fixes = self.fixup(child)
            if index == 0:
                self.first_node = child
        elif index == self.length():
            node = self.get(index)
            child = AVLNode(val, node)
            node.right = child
            fixes = self.fixup(child)
            self.last_node = child

        return fixes

    def delete(self, index):
        """
        Deletes the ith item in the list.
        Complexity: O(log(n)).

        @type index: int
        @pre: 0 <= index < self.length()
        @param index: The intended index in the list to be deleted
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        """
        if index > self.length():
            return -1

        node = self.get(index + 1)
        if node.isLeafNode():
            return self.delete_leaf_node(node)
        elif node.left.isVirtualNode() ^ node.right.isVirtualNode():
            return self.delete_node_with_one_child(node)
        else:
            return self.delete_node_with_two_children(node)

    def delete_leaf_node(self, node):
        """
        Delete the given node, while assuming it's a leaf node.
        Simply deletes the node, and replaces it with a virtual node.
        Complexity: O(log(n)).

        @type node: AVLNode
        @param node: The node to delete.
        @rtype: int
        @return: The number of fix operations done.
        """
        parent = node.parent
        node.parent = None
        if parent is None:
            self.root = AVLNode()
            self.first_node = self.last_node = self.root
        elif parent.left == node:
            parent.left = AVLNode(parent=parent)
            if self.first_node == node:
                self.first_node = parent
        else:
            parent.right = AVLNode(parent=parent)
            if self.last_node == node:
                self.last_node = parent
        return self.fixup(parent)

    def delete_node_with_one_child(self, node):
        """
        Delete the given node, while assuming it has one child, by setting the node to its single child.
        Complexity: O(log(n)).

        @type node: AVLNode
        @param node: The node to delete.
        @rtype: int
        @return: The number of fix operations done.
        """
        parent = node.parent
        if node.left.isRealNode():
            child = node.left
            if self.last_node == node:
                self.last_node = child
        else:
            child = node.right
            if self.first_node == node:
                self.first_node = child

        child.parent = parent
        node.parent = None

        if parent is None:
            self.root = child
        elif parent.left == node:
            parent.left = child
        else:
            parent.right = child

        return self.fixup(parent)

    def delete_node_with_two_children(self, node):
        """
        Delete the given node, while assuming it has two children.
        Finds the successor of the node, which we know doesn't have a left child, and handles it according to the two
        previous cases.
        Complexity: O(log(n)).

        @type node: AVLNode
        @param node: The node to delete.
        @rtype: int
        @return: The number of fix operations done.
        """
        successor = node.getSuccessor()
        node.value = successor.value
        if successor.right.isRealNode():
            return self.delete_node_with_one_child(successor)
        return self.delete_leaf_node(successor)

    def first(self):
        """
        Returns the value of the first item in the list.
        Complexity: O(1).

        @rtype: str
        @returns: The value of the first item, None if the list is empty
        """
        return self.first_node.value if self.first_node.isRealNode() else None

    def last(self):
        """
        Returns the value of the last item in the list.
        Complexity: O(1).

        @rtype: str
        @returns: The value of the last item, None if the list is empty
        """
        return self.last_node.value if self.last_node.isRealNode() else None

    def listToArray(self):
        """
        Returns an array representing list.
        Complexity: O(n).

        @rtype: list
        @returns: a list of strings representing the data structure
        """
        arr = []
        self._listToArrayRec(self.root, arr)
        return arr

    def _listToArrayRec(self, node, lst):
        """
        An internal function that traverses the tree inorder, and adds all node values to the given list.
        Complexity: O(n).

        @type node: AVLNode
        @param node: The node to start the inorder traversal from.
        @type lst: list
        @param lst: The list to add the values to.
        """
        if node.isRealNode():
            self._listToArrayRec(node.left, lst)
            lst.append(node.value)
            self._listToArrayRec(node.right, lst)

    def length(self):
        """
        Returns the size of the list.
        Complexity: O(1).

        @rtype: int
        @returns: the size of the list
        """
        return self.root.rank

    def split(self, index):
        """
        Splits the list at the ith index.
        Complexity: O(log(n)).

        @type index: int
        @pre: 0 <= i < self.length()
        @param index: The intended index in the list according to whom we split
        @rtype: list
        @returns: A list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
        right is an AVLTreeList representing the list from index i+1, and val is the value at the ith index.
        """
        node = self.get(index + 1)
        val = node.value

        small_tree = AVLTreeList(node.left, remove_parent_from_root=True)
        large_tree = AVLTreeList(node.right, remove_parent_from_root=True)

        nodes_list, sides_list = [], []
        while node.parent is not None:
            nodes_list.append(node.parent)
            sides_list.append(node.isParentRight())
            node = node.parent

        for i, node in enumerate(nodes_list):
            node.parent = None
            if sides_list[i]:
                large_tree.concatWithAxis(
                    AVLTreeList(node.right, remove_parent_from_root=True), node
                )
            else:
                temp_tree = AVLTreeList(node.left, remove_parent_from_root=True)
                temp_tree.concatWithAxis(small_tree, node)
                small_tree = temp_tree

        return [small_tree, val, large_tree]

    def concat(self, lst):
        """
        Concatenates lst to self.
        Complexity: O(log(n)).

        @type lst: AVLTreeList
        @param lst: a list to be concatenated after self
        @rtype: int
        @returns: the absolute value of the difference between the height of the AVL trees joined
        """
        height_diff = self.root.height - lst.root.height
        if lst.empty():
            return abs(height_diff)
        if self.empty():
            self.root = lst.root
            self.first_node, self.last_node = lst.first_node, lst.last_node
            return abs(height_diff)

        axis = self.get(self.length())
        self.delete(self.length() - 1)
        self.concatWithAxis(lst, axis)
        return abs(height_diff)

    def concatWithAxis(self, lst, axis):
        """
        Concatenates the lst to self with the given axis value.
        Complexity: O(log(n)).

        @type lst: AVLTreeList
        @param lst: The list to concatenate to self.
        @type axis: AVLNode
        @param axis: The axis node to concatenate with.
        """
        height_diff = self.root.height - lst.root.height
        if lst.empty():
            self.insert(self.length(), axis.value)
            self.last_node = self.get(self.length())
            return
        elif self.empty():
            lst.insert(0, axis.value)
            self.root = lst.root
            self.first_node, self.last_node = lst.first_node, lst.last_node
            return
        elif height_diff == 0:
            axis.setLeft(self.root)
            axis.setRight(lst.root)
            self.root = axis
        elif height_diff < 0:
            node = lst.root
            while node.height > self.root.height:
                node = node.left
            axis.setLeft(self.root)
            node.parent.setLeft(axis)
            axis.setRight(node)
            self.root = lst.root
        else:
            node = self.root
            while node.height > lst.root.height:
                node = node.right
            axis.setRight(lst.root)
            node.parent.setRight(axis)
            axis.setLeft(node)
        self.last_node = lst.last_node
        self.fixup(axis)
        return abs(height_diff)

    def search(self, val):
        """
        Searches for the given in the list and return its index.
        Complexity: O(n).

        @type val: str
        @param val: A value to be searched
        @rtype: int
        @returns: The first index that contains val, -1 if not found.
        """
        return self._searchRec(val, index=0, node=self.root)

    def _searchRec(self, val, index, node):
        """
        A utility function to start searching the given value from the given node.
        Complexity: O(n).

        @type val: str
        @param val: The value to search in the list.
        @type index: int
        @param index: The index to add to the search result.
        @type node: AVLNode
        @param node: The node to start the search from.
        @return: The index of the value, or -1 if not found.
        """
        if node is None or node.isVirtualNode():
            return -1

        left = self._searchRec(val, index, node.left)
        if left != -1:
            return left
        if node.value == val:
            return index + node.left.rank
        return self._searchRec(val, index + node.left.rank + 1, node.right)

    def getRoot(self):
        """
        Returns the root of the tree representing the list.
        Complexity: O(1).

        @rtype: AVLNode
        @returns: The root, None if the list is empty.
        """
        return self.root

    def get(self, index):
        """
        Returns a pointer to the ith node (starts with index 1).
        Complexity: O(log(n)).

        @rtype: AVLNode
        @returns: The ith node, or None if the tree is smaller
        """
        node = self.root
        if index > node.rank or 1 > index:
            raise IndexError("index out of range")
        while node.left.rank != index - 1:
            if node.left.rank >= index:
                node = node.left
            else:
                index -= node.left.rank + 1
                node = node.right
        return node

    def rightRotation(self, node):
        """
        Performs a right rotation around the given node.
        Complexity: O(1).

        @type node: AVLNode
        @param node: The node to rotate around.
        """
        new_parent = node.left
        node.left = new_parent.right
        node.left.parent = node
        new_parent.right = node
        new_parent.parent = node.parent

        if new_parent.parent is None:
            self.root = new_parent
        elif new_parent.parent.right == node:
            new_parent.parent.right = new_parent
        else:
            new_parent.parent.left = new_parent

        node.parent = new_parent
        node.update()

    def leftRotation(self, node):
        """
        Performs a left rotation around the given node.
        Complexity: O(1).

        @type node: AVLNode
        @param node: The node to rotate around.
        """
        new_parent = node.right
        node.right = new_parent.left
        node.right.parent = node
        new_parent.left = node
        new_parent.parent = node.parent

        if new_parent.parent is None:
            self.root = new_parent
        elif new_parent.parent.right == node:
            new_parent.parent.right = new_parent
        else:
            new_parent.parent.left = new_parent

        node.parent = new_parent
        node.update()

    def fixNode(self, node):
        """
        Fixes the single given node, and returns the number of operations done.
        Complexity: O(1).

        @type node: AVLNode
        @param node: The node to fixup.
        @returns: Number of fixup operations done.
        """
        updates = node.update()
        if node.balanceFactor == 2:
            if node.left.balanceFactor >= 0:
                self.rightRotation(node)
                return 1
            else:
                self.leftRotation(node.left)
                self.rightRotation(node)
                return 2
        elif node.balanceFactor == -2:
            if node.right.balanceFactor <= 0:
                self.leftRotation(node)
                return 1
            else:
                self.rightRotation(node.right)
                self.leftRotation(node)
                return 2
        return updates

    def fixup(self, node):
        """
        Goes up the tree from a given node after insertion or deletion and makes the required rotation actions to
        maintain the balance of the tree, and then returns how many rotations were done.
        Complexity: O(log(n)).

        @rtype: int
        @returns: Number of operations done.
        """
        fixes = 0
        while node is not None:
            fixes += self.fixNode(node)
            node = node.parent
        return fixes
