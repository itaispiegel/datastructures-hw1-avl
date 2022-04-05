import random

from datastructure_hw1_avl.avl import AVLTreeList


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(
        ls * " "
        + (lwid - ls) * "_"
        + "/"
        + rootwid * " "
        + "\\"
        + rs * "_"
        + (rwid - rs) * " "
    )

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def trepr(t, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if t is None:
        return ["#"]

    thistr = str(t.value)

    return conc(trepr(t.left, bykey), thistr, trepr(t.right, bykey))


def printree(t, bykey=True):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    for row in trepr(t, bykey):
        print(row)
    # return trepr(t, bykey)


def randomTree(ops):
    t = AVLTreeList()
    for i in range(ops):
        if t.empty() or random.random() > 0.3:
            t.insert(random.randrange(t.length() + 1), i)
        else:
            t.delete(random.randrange(t.length()))
        printree(t.root, False)
    return t


if __name__ == "__main__":
    randomTree(10)
