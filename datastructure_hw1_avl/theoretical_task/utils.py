import random
from typing import Tuple

from datastructure_hw1_avl.avl import AVLTreeList


def insert_items_to_avl_tree_list(tree_list: AVLTreeList, size: int) -> int:
    operations = 0
    for i in range(size):
        value = str(i)
        index = random.randint(0, tree_list.length())
        operations += tree_list.insert(index, value)
    return operations


def create_random_tree_list(tree_size: int) -> Tuple[int, AVLTreeList]:
    tree_list = AVLTreeList()
    return insert_items_to_avl_tree_list(tree_list, tree_size), tree_list


def delete_random_item_from_tree(tree_list: AVLTreeList) -> int:
    index = random.randint(0, tree_list.length() - 1)
    return tree_list.delete(index)


def delete_all_items_from_tree(tree_list: AVLTreeList) -> int:
    operations = 0
    while tree_list.length() > 0:
        operations += delete_random_item_from_tree(tree_list)
    return operations


def insert_and_remove_items(tree_list: AVLTreeList, actions_count: int) -> int:
    operations = 0
    for i in range(actions_count):
        should_insert = bool(random.getrandbits(1))
        if should_insert:
            operations += insert_items_to_avl_tree_list(tree_list, 1)
        else:
            operations += delete_all_items_from_tree(tree_list)
    return operations
