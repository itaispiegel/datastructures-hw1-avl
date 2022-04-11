import random
import string
from test.conftest import LARGE_TREE_SIZE
from typing import Any, List, Tuple

from datastructure_hw1_avl.avl import AVLTreeList

ITERATIONS = 1000
RANDOM_STRINGS_SIZE = 15

# This random seed causes the bug deterministically :(
random.seed(19)


def _test_list_insert(avl_tree: AVLTreeList, equivalent_list: List[str]):
    index = random.randint(0, avl_tree.length())
    new_item = "".join(random.choices(string.ascii_lowercase + string.digits, k=RANDOM_STRINGS_SIZE))
    avl_tree.insert(index, new_item)
    equivalent_list.insert(index, new_item)


def _test_list_remove(avl_tree: AVLTreeList, equivalent_list: List[str]):
    index = random.randint(0, avl_tree.length() - 1)
    avl_tree.delete(index)
    equivalent_list.pop(index)


def _test_list_search(
    avl_tree: AVLTreeList, equivalent_list: List[str]
) -> Tuple[Any, Any]:
    item = random.choice(equivalent_list)
    return avl_tree.search(item), equivalent_list.index(item)


def test_large_tree(large_tree: AVLTreeList):
    equivalent_list = list(str(i) for i in range(LARGE_TREE_SIZE))
    list_operations = [_test_list_insert, _test_list_remove, _test_list_search]

    for i in range(ITERATIONS):
        test_operation = random.choice(list_operations)
        result = test_operation(large_tree, equivalent_list)
        if result is not None:
            r1, r2 = result
            assert r1 == r2
        assert (
            equivalent_list == large_tree.listToArray()
        ), f"Failed after {i} iterations at operation: {test_operation.__name__}"
