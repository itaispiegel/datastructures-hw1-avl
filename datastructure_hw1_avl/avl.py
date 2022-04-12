# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info


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

    def getLeft(self):
        """
        Returns the left child

        @rtype: AVLNode
        @returns: The left child of self, None if there is no left child
        """
        if self.isRealNode():
            return self.left
        return None

    def getRight(self):
        """
        Returns the right child

        @rtype: AVLNode
        @returns: The right child of self, None if there is no right child
        """
        if self.isRealNode():
            return self.right
        return None

    def getParent(self):
        """
        Returns the parent

        @rtype: AVLNode
        @returns: The parent of self, None if there is no parent
        """
        return self.parent

    def getValue(self):
        """
        Return the value

        @rtype: str
        @returns: The value of self, None if the node is virtual
        """
        return self.value

    def getHeight(self):
        """
        Returns the height

        @rtype: int
        @returns: The height of self, -1 if the node is virtual
        """
        return self.height

    def setLeft(self, node):
        """
        Sets left child

        @type node: AVLNode
        @param node: a node
        """
        self.left = node
        node.setParent(self)

    def setRight(self, node):
        """
        Sets right child

        @type node: AVLNode
        @param node: a node
        """
        self.right = node
        node.setParent(self)

    def setParent(self, node):
        """
        Sets parent

        @type node: AVLNode
        @param node: a node
        """
        self.parent = node

    def setValue(self, value):
        """
        Sets value

        @type value: str
        @param value: data
        """
        self.value = value

    def setHeight(self, h):
        """
        Sets the height of the node

        @type h: int
        @param h: the height
        """
        self.height = h

    def isRealNode(self):
        """
        Returns whether self is a real node

        @rtype: bool
        @returns: True iff self is a real node.
        """
        return self.height != -1

    def isVirtualNode(self):
        """
        Returns whether self is a virtual node

        @rtype: bool
        @returns: True iff self is a virtual node.
        """
        return not self.isRealNode()

    def update(self):
        """
        Update the node's fields from its children.

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

        @rtype: bool
        @returns: True iff the node's parent is to the right of it.
        """
        return self.parent is not None and self.parent.left == self

    @property
    def balanceFactor(self):
        """
        Returns the balance factor of the given node, which is the difference in height of the left node and the right.

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

    def __init__(self, root=None):
        """Constructor, you are allowed to add more fields."""
        self.root = root or AVLNode()
        # add your fields here

    def empty(self):
        """
        Returns whether the list is empty

        @rtype: bool
        @returns: True if the list is empty, False otherwise
        """
        return self.root.isVirtualNode()

    def retrieve(self, index):
        """
        Retrieves the value of the ith item in the list

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
        Inserts val at position i in the list

        @type index: int
        @pre: 0 <= index <= self.length()
        @param index: The intended index in the list to which we insert val
        @type val: str
        @param val: the inserted value
        @rtype: list
        @returns: The number of re-balance operation due to AVL re-balancing.
        """
        fixes = 0
        if index > self.length():
            return fixes
        elif self.empty() and index == 0:
            self.root = AVLNode(val)
            return fixes
        elif index <= self.length() - 1:
            node = self.get(index + 1)
            if node.left.isVirtualNode():
                child = AVLNode(val, node)
                node.left = child
            else:
                pred = self.getPred(node)
                child = AVLNode(val, pred)
                pred.right = child
            fixes = self.fixup(child)
        elif index == self.length():
            node = self.get(index)
            child = AVLNode(val, node)
            node.right = child
            fixes = self.fixup(child)

        return fixes

    def delete(self, index):
        """
        Deletes the ith item in the list

        @type index: int
        @pre: 0 <= index < self.length()
        @param index: The intended index in the list to be deleted
        @rtype: int
        @returns: the number of rebalancing operation due to AVL rebalancing
        """
        if index > self.length():
            return -1

        node = self.get(index + 1)
        if node.left.isVirtualNode():
            node.right.parent = node.parent
            if node == self.root:
                self.root = node.right
                return 0
            elif node.isParentRight():
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            fixes = self.fixup(node.parent)
            return fixes

        pred = self.getPred(node)
        node.value = pred.value
        if pred.isParentRight():
            pred.parent.left = pred.left
        else:
            pred.parent.right = pred.left
        pred.left.parent = pred.parent
        fixes = self.fixup(pred.parent)
        return fixes

    def first(self):
        """
        Returns the value of the first item in the list

        @rtype: str
        @returns: The value of the first item, None if the list is empty
        """
        node = self.root
        while node.isRealNode() and node.left.isRealNode():
            node = node.left
        return node.value

    def last(self):
        """
        Returns the value of the last item in the list

        @rtype: str
        @returns: The value of the last item, None if the list is empty
        """
        node = self.root
        while node.isRealNode() and node.right.isRealNode():
            node = node.right
        return node.value

    def listToArray(self):
        """
        Returns an array representing list

        @rtype: list
        @returns: a list of strings representing the data structure
        """
        arr = []
        self._listToArrayRec(self.root, arr)
        return arr

    def _listToArrayRec(self, node, lst):
        """
        An internal function that traverses the tree inorder, and adds all node values to the given list.

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
        Returns the size of the list

        @rtype: int
        @returns: the size of the list
        """
        return self.root.rank

    def split(self, index):
        """
        Splits the list at the ith index.

        @type index: int
        @pre: 0 <= i < self.length()
        @param index: The intended index in the list according to whom we split
        @rtype: list
        @returns: A list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
        right is an AVLTreeList representing the list from index i+1, and val is the value at the ith index.
        """
        node = self.get(index + 1)
        val = node.value
        smallTree = AVLTreeList(node.left)
        bigTree = AVLTreeList(node.right)

        while node.parent is not None:
            if node.isParentRight():
                bigTree.join(AVLTreeList(node.parent.right), node.parent)
            else:
                tempTree = AVLTreeList(node.parent.left).join(smallTree, node.parent)
                smallTree = tempTree
            node = node.parent

        return [smallTree, val, bigTree]

    def concat(self, lst):
        """
        Concatenates lst to self

        @type lst: AVLTreeList
        @param lst: a list to be concatenated after self
        @rtype: int
        @returns: the absolute value of the difference between the height of the AVL trees joined
        """
        original_height_diff = self.root.height - lst.root.height
        if lst.empty():
            return abs(original_height_diff)
        if self.empty():
            self.root = lst.root
            return abs(original_height_diff)

        axis = self.get(self.length())
        self.delete(self.length() - 1)
        self.join(lst, axis)
        return abs(original_height_diff)

    def join(self, lst, axis):
        if lst.empty():
            self.insert(self.length(), axis)
            return
        elif self.empty():
            lst.insert(0, axis)
            self.root = lst.root
            return
        height_diff = self.root.height - lst.root.height
        if height_diff == 0:
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

        self.fixup(axis)

    def search(self, val, index=0, node=None):
        """
        Searches for the given in the list and return its index.

        @type val: str
        @param val: A value to be searched
        @rtype: int
        @returns: The first index that contains val, -1 if not found.
        """
        if node is None:
            node = self.root

        if node.isVirtualNode():
            return -1
        left = self.search(val, index, node.left)
        if left != -1:
            return left
        if node.value == val:
            return index + node.left.rank

        right = self.search(val, index + node.left.rank + 1, node.right)
        return right

    def getRoot(self):
        """
        Returns the root of the tree representing the list.

        @rtype: AVLNode
        @returns: The root, None if the list is empty.
        """
        return self.root

    def get(self, index):
        """
        Returns a pointer to the ith node (starts with index 1).
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

    def getPred(self, node):
        """
        Returns the predecessor node.
        @rtype: AVLNode
        @returns: The node with index - 1, or None if none exist (first item).
        """
        if node.left.isRealNode():
            node = node.left
            while node.right.isRealNode():
                node = node.right
            return node
        else:
            while node.parent is not None and node.isParentRight():
                node = node.parent
            return node.parent

    def rightRotation(self, node):
        """
        Performs a right rotation around the given node.

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

        @type node: AVLNode
        @param node: The node to fixup.
        @returns: Number of fixup operations done.
        """
        updates = node.update()
        if node.balanceFactor == 2:
            if node.left.balanceFactor == 1:
                self.rightRotation(node)
                return 1
            else:
                self.leftRotation(node.left)
                self.rightRotation(node)
                return 2
        elif node.balanceFactor == -2:
            if node.right.balanceFactor == -1:
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

        @rtype: int
        @returns: Number of operations done.
        """
        fixes = 0
        while node is not None:
            fixes += self.fixNode(node)
            node = node.parent
        return fixes
