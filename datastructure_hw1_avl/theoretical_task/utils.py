import random
import sys
from contextlib import contextmanager
from typing import List, Tuple, Type

from datastructure_hw1_avl.avl import AVLTreeList


def insert_item_to_random_index_in_tree_list(tree_list: AVLTreeList, value: str) -> int:
    index = random.randint(0, tree_list.length())
    return tree_list.insert(index, value)


def insert_random_items_to_avl_tree_list(tree_list: AVLTreeList, size: int) -> int:
    operations = 0
    for i in range(size):
        operations += insert_item_to_random_index_in_tree_list(tree_list, str(i))
    return operations


def create_random_tree_list(
    tree_size: int, tree_type=AVLTreeList
) -> Tuple[int, AVLTreeList]:
    tree_list = tree_type()
    return insert_random_items_to_avl_tree_list(tree_list, tree_size), tree_list


def create_tree_from_list(
    lst: List[str], tree_type: Type[AVLTreeList] = AVLTreeList
) -> AVLTreeList:
    avl_tree = tree_type()
    for i, item in enumerate(lst):
        avl_tree.insert(i, item)
    return avl_tree


def delete_random_item_from_tree(tree_list: AVLTreeList) -> int:
    index = random.randint(0, tree_list.length() - 1)
    return tree_list.delete(index)


def delete_all_items_from_tree(tree_list: AVLTreeList) -> int:
    operations = 0
    while tree_list.length() > 0:
        operations += delete_random_item_from_tree(tree_list)
    return operations


def insert_and_remove_items_randomly(tree_list: AVLTreeList, actions_count: int) -> int:
    operations = 0
    for i in range(actions_count):
        should_insert = bool(random.getrandbits(1))
        if should_insert:
            operations += insert_random_items_to_avl_tree_list(tree_list, 1)
        else:
            operations += delete_all_items_from_tree(tree_list)
    return operations


@contextmanager
def set_recursion_limit(new_limit: int):
    original_recursion_limit = sys.getrecursionlimit()
    try:
        sys.setrecursionlimit(new_limit)
        yield
    finally:
        sys.setrecursionlimit(original_recursion_limit)
