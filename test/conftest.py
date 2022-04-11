import string

import pytest

from datastructure_hw1_avl.avl import AVLTreeList

LARGE_TREE_SIZE = 500


@pytest.fixture
def empty_tree():
    return AVLTreeList()


@pytest.fixture
def small_tree():
    tree = AVLTreeList()
    for i in range(4):
        tree.insert(i, string.ascii_lowercase[i])
    return tree


@pytest.fixture
def large_tree():
    tree = AVLTreeList()
    for i in range(LARGE_TREE_SIZE):
        tree.insert(i, str(i))
    return tree
