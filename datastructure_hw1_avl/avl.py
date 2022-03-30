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

    def setRight(self, node):
        """
        Sets right child

        @type node: AVLNode
        @param node: a node
        """
        self.right = node

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
        Sets the balance factor of the node

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


class AVLTreeList(object):
    """
    A class implementing the ADT list, using an AVL tree.
    """

    def __init__(self):
        """Constructor, you are allowed to add more fields."""
        self.root = AVLNode()
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
        if index < self.root.rank:
            node = self.getIth(index + 1)
            return node.value
        return None

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
        if self.empty() and index == 0:
            self.root = AVLNode(val)
            return 0
        elif index <= self.length() - 1:
            node = self.getIth(index + 1)
            if node.left.isVirtualNode():
                node.left = AVLNode(val, node)
                node = node.left
            else:
                node = self.getPred(node)
                node.right = AVLNode(val, node)
                node = node.right
            fixes = self.fixup(node)
            return fixes
        elif index == self.length():
            node = self.getIth(index)
            node.right = AVLNode(val, node)
            fixes = self.fixup(node)
            return fixes

        return -1

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
        node = self.getIth(index + 1)
        if self.root == node:
            if node.left.isVirtualNode():
                self.root = node.right
                self.root.parent = None
                return 0

            if node.left.isVirtualNode():
                node.right.parent = node.parent
                if node == self.root:
                    self.root = node.right
                    return 0
                elif self.isParentRight(node):
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
                fixes = self.fixup(node.parent)
                return fixes

            pred = self.getPred(node)
            node.value = pred.value
            if self.isParentRight(pred):
                pred.parent.left = AVLNode()
            else:
                pred.parent.right = AVLNode()
            fixes = self.fixup(pred.parent)
            return fixes
        return -1

    def first(self):
        """
        Returns the value of the first item in the list

        @rtype: str
        @returns: The value of the first item, None if the list is empty
        """
        node = self.root
        while node.left.isRealNode():
            node = node.left
        return node.value

    def last(self):
        """
        Returns the value of the last item in the list

        @rtype: str
        @returns: The value of the last item, None if the list is empty
        """
        node = self.root
        while node.right.isRealNode():
            node = node.right
        return node.value

    def listToArray(self):
        """
        Returns an array representing list

        @rtype: list
        @returns: a list of strings representing the data structure
        """
        arr = self._listToArrayRec(self, self.root)
        return arr

    def _listToArrayRec(self, node):
        if node.isVirtualNode():
            return []
        arr = self._listToArrayRec(node.left)
        arr.append(node.value)
        for i in self._listToArrayRec(node.right):
            arr.append(i)
        return arr

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
        return None

    def concat(self, lst):
        """
        Concatenates lst to self

        @type lst: AVLTreeList
        @param lst: a list to be concatenated after self
        @rtype: int
        @returns: the absolute value of the difference between the height of the AVL trees joined
        """
        if lst.empty():
            return self.root.height
        if self.empty():
            self.root = lst.root
            return self.root.height

        h_diff = self.root.height - lst.root.height
        if self.root.height > lst.root.height:
            axis = self.getIth(self.length())
            self.delete(self.length() - 1)
        else:
            axis = lst.getIth(1)
            lst.delete(0)
        if h_diff < 0:
            node = lst.root
            while node.height > self.root.height:
                node = node.left
            axis.left = self.root
            self.root.parent = axis
            axis.right = node
            node.parent.left = axis
            node.parent = axis
            self.root = lst.root
        else:
            node = self.root
            while node.height > lst.root.height:
                node = node.right
            axis.right = lst.root
            lst.root.parent = axis
            axis.left = node
            node.parent.right = axis
            node.parent = axis

        self.fixup(axis)

        return abs(h_diff)

    def search(self, val):
        """
        Searches for the given in the list and return its index.

        @type val: str
        @param val: A value to be searched
        @rtype: int
        @returns: The first index that contains val, -1 if not found.
        """
        return None

    def getRoot(self):
        """
        Returns the root of the tree representing the list.

        @rtype: AVLNode
        @returns: The root, None if the list is empty.
        """
        return self.root

    def getIth(self, index):
        """
        Returns a pointer to the ith node.
        @rtype: AVLNode
        @returns: The ith node, or None if the tree is smaller
        """
        node = self.root
        if index > node.rank:
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
            while node.parent is not None and self.isParentRight(node):
                node = node.parent
            return node.parent

    def rotate(self, node, side):
        """
        Rotates the tree to maintain balance.

        @rtype: None
        @returns: None
        """

        # To avoid code duplication, we define lambda functions that
        # 'reverse' the sides if needed, and then the rest is written as
        # if this is a right rotation, where all relevant directions
        # are reversed in the left rotation
        if side == 1:  # if the rotation is to the right
            gRight = AVLNode.getRight
            gLeft = AVLNode.getLeft
            sRight = AVLNode.setRight
            sLeft = AVLNode.setLeft
        else:  # if the rotation is to the left, reverse all directions
            gRight = AVLNode.getLeft
            gLeft = AVLNode.getRight
            sRight = AVLNode.setLeft
            sLeft = AVLNode.setRight
        A = gLeft(node)
        par = node.parent
        sLeft(node, gRight(A))
        sRight(A, node)

        # The side the original node is to its parent is not
        # related to the direction of the rotation, which is why
        # we don't use the lambda functions but the actual fields
        if node == self.root:
            self.root = A
        elif self.isParentRight(node):
            node.parent.left = A
        else:
            node.parent.right = A

        node.parent = A
        A.parent = par
        l = gLeft(node)
        l.parent = node
        node.rank = node.left.rank + node.right.rank + 1
        node.height = max(node.left.height, node.right.height) + 1
        A.rank = A.left.rank + A.right.rank + 1
        A.height = max(A.left.height, A.right.height) + 1

    def fixup(self, node):
        """
        Goes up the tree from a given node after insertion or deletion and makes the required rotation actions to
        maintain the balance of the tree, and then returns how many rotations were done.

        @rtype: int
        @returns: Number of rotations done.
        """
        fixes = 0
        while node is not None:
            node.height = max(node.left.height, node.right.height) + 1
            node.rank = node.left.rank + node.right.rank + 1
            BL = node.left.height - node.right.height
            if BL == 2:
                if node.left.left.height - node.left.right.height == 1:
                    self.rotate(node, 1)
                    fixes += 1
                else:
                    self.rotate(node.left, 0)
                    self.rotate(node, 1)
                    fixes += 2
            elif BL == -2:
                if node.right.left.height - node.right.right.height == -1:
                    self.rotate(node, 0)
                    fixes += 1
                else:
                    self.rotate(node.right, 1)
                    self.rotate(node, 0)
                    fixes += 2
            node = node.parent
        return fixes

    def isParentRight(self, node):
        """
        Checks if the given node's parent is to its left or right.

        @rtype: bool
        @returns: True iff the node's parent is to the right of it.
        """
        return node.parent is not None and node.parent.left == node
