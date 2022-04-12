import random
import string
from test.conftest import LARGE_TREE_SIZE
from typing import Any, List, Optional, Tuple

from datastructure_hw1_avl.avl import AVLNode, AVLTreeList

ITERATIONS = 1000
RANDOM_STRINGS_SIZE = 15
RANDOM_LIST_MAX_SIZE = 100


def _generate_random_string() -> str:
    return "".join(
        random.choices(string.ascii_lowercase + string.digits, k=RANDOM_STRINGS_SIZE)
    )


def _generate_random_list():
    size = random.randint(1, RANDOM_LIST_MAX_SIZE)
    return [_generate_random_string() for _ in range(size)]


def _create_avl_tree_list_from_list(lst: List[str]) -> AVLTreeList:
    avl_tree = AVLTreeList()
    for i, item in enumerate(lst):
        avl_tree.insert(i, item)
    return avl_tree


def _get_node_with_bad_balance_factor(node: AVLNode) -> Optional[AVLNode]:
    if node.isVirtualNode():
        return None
    left = _get_node_with_bad_balance_factor(node.left)
    if left is not None:
        return left
    if abs(node.balanceFactor) > 2:
        return node
    return _get_node_with_bad_balance_factor(node.right)


def _test_list_insert(avl_tree: AVLTreeList, equivalent_list: List[str]):
    index = random.randint(0, avl_tree.length())
    new_item = _generate_random_string()
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


def _test_list_concat(avl_tree: AVLTreeList, equivalent_list: List[str]):
    random_list = _generate_random_list()
    random_avl_tree = _create_avl_tree_list_from_list(random_list)

    avl_tree.concat(random_avl_tree)
    equivalent_list.extend(random_list)


def test_large_tree(large_tree: AVLTreeList):
    equivalent_list = list(str(i) for i in range(LARGE_TREE_SIZE))
    list_operations = [_test_list_insert, _test_list_remove, _test_list_search, _test_list_concat]

    for i in range(ITERATIONS):
        test_operation = random.choice(list_operations)
        result = test_operation(large_tree, equivalent_list)
        if result is not None:
            r1, r2 = result
            assert r1 == r2
        assert (
            equivalent_list == large_tree.listToArray()
        ), f"Failed after {i} iterations at operation: {test_operation.__name__}"

        bad_node = _get_node_with_bad_balance_factor(large_tree.root)
        assert bad_node is None