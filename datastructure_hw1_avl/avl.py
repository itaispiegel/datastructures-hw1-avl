# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - complete info
# name2    - complete info

"""A class representing a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.rank = 0

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    """

    def getLeft(self):
        if self.isRealNode():
            return self.left
        return None

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        if self.isRealNode():
            return self.right
        return None

    """returns the parent

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is a real node

    @rtype: bool
    @returns: True iff self is a real node.
    """

    def isRealNode(self):
        return self.height != -1

    """returns whether self is a virtual node

    @rtype: bool
    @returns: True iff self is a virtual node.
    """

    def isVirtualNode(self):
        return not self.isRealNode()


"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = AVLNode(None)
        # add your fields here

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    """

    def empty(self):
        return self.root.isVirtualNode()

    """retrieves the value of the i'th item in the list

    @type index: int
    @pre: 0 <= index < self.length()
    @param index: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, index):
        if index < self.root.rank:
            node = self.getIth(index + 1)
            return node.value
        return None

    """inserts val at position i in the list

    @type index: int
    @pre: 0 <= index <= self.length()
    @param index: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def insert(self, index, val):
        if self.empty() and index == 0:
            self.root = self.newNode(None, val)
            return 0
        elif index <= self.length() - 1:
            node = self.getIth(index + 1)
            if node.left.isVirtualNode():
                node.left = self.newNode(node, val)
                node = node.left
            else:
                node = self.getPred(node)
                node.right = self.newNode(node, val)
                node = node.right
            fixes = self.fixup(node)
            return fixes
        elif index == self.length():
            node = self.getIth(index)
            node.right = self.newNode(node, val)
            fixes = self.fixup(node)
            return fixes

        return -1

    """deletes the i'th item in the list

    @type index: int
    @pre: 0 <= index < self.length()
    @param index: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, index):
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
                pred.parent.left = AVLNode(None)
            else:
                pred.parent.right = AVLNode(None)
            fixes = self.fixup(pred.parent)
            return fixes
        return -1

    """returns the value of the first item in the list

    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        node = self.root
        while node.left.isRealNode():
            node = node.left
        return node.value

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        node = self.root
        while node.right.isRealNode():
            node = node.right
        return node.value

    """returns an array representing list

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    def listToArray(self):
        arr = self.listToArrayRec(self, self.root)
        return arr

    def listToArrayRec(self, node):
        if node.isVirtualNode():
            return []
        arr = self.listToArrayRec(node.left)
        arr.append(node.value)
        for i in self.listToArrayRec(node.right):
            arr.append(i)
        return arr

    """returns the size of the list

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.root.rank

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    """

    def split(self, index):
        return None

    """concatenates lst to self

    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    """

    def concat(self, lst):
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

    """searches for a *value* in the list

    @type val: str
    @param val: a value to be searched
    @rtype: int
    @returns: the first index that contains val, -1 if not found.
    """

    def search(self, val):
        return None

    """returns the root of the tree representing the list

    @rtype: AVLNode
    @returns: the root, None if the list is empty
    """

    def getRoot(self):
        return self.root

    """returns a pointer to the ith node
    @rtype: AVLNode
    @returns: the ith node, or None if the tree is smaller
    """

    def getIth(self, index):
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

    """returns the predecessor node
    @rtype: AVLNode
    @returns: the node with index-1, or None if none exist (first item)
    """

    def getPred(self, node):
        if node.left.isRealNode():
            node = node.left
            while node.right.isRealNode():
                node = node.right
            return node
        else:
            while node.parent is not None and self.isParentRight(node):
                node = node.parent
            return node.parent

    """ initializes a new non-vitual node
    @rtype: AVLNode
    @returns: the new node after its initialized
    """

    def newNode(self, parent, val):
        node = AVLNode(val)
        node.left = AVLNode(None)
        node.right = AVLNode(None)
        node.rank = 1
        node.height = 0
        node.parent = parent
        return node

    """ rotates the tree to maintain balance
    @rtypeL None
    @returns: None
    """

    def rotate(self, node, side):
        """To avoid code duplication, we define lambda functions that
        'reverse' the sides if needed, and then the rest is written as
        if this is a right rotation, where all relevant directions
        are reversed in the left rotation
        """
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

        """The side the original node is to its parent is not
        related to the direction of the rotation, which is why
        we don't use the lambda functions but the actual fields
        """
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

    """this functions goes up the tree from a given node after insertion
    or deletion and makes the needed rotation actions to maintain the
    balance of the tree, and then returns how many rotations were needed
    @rtype: int
    @returns: how many rotations were needed
    """

    def fixup(self, node):
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

    """this function checks if the given node's parent is to its left or right
    @rtype: bool
    @returns: true if it's on the right side (if its hte parents right child,
    false if its the right, and none if it has no parent
    """

    def isParentRight(self, node):
        return node.parent is not None and node.parent.left == node
