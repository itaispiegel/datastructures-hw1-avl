import math
from typing import Tuple

from datastructure_hw1_avl.avl import AVLTreeList
from datastructure_hw1_avl.theoretical_task.utils import (
    insert_item_to_random_index_in_tree_list,
    set_recursion_limit,
)

SIZES = [1000 * i for i in range(1, 11)]


class BinarySearchTreeList(AVLTreeList):
    def fixNode(self, node):
        return node.update()


def create_arithmetic_progressing_tree_list(size: int) -> Tuple[float, float, float, float]:
    avl_tree_list, non_avl_tree_list = AVLTreeList(), BinarySearchTreeList()
    avl_operations, non_avl_operations = 0, 0
    avl_depths_sum, non_avl_depths_sum = 0, 0
    for i in range(size):
        value = str(i)
        avl_operations += avl_tree_list.insert(0, value)
        inserted_node = avl_tree_list.get(avl_tree_list.search(value) + 1)
        avl_depths_sum += inserted_node.depth()

        non_avl_operations += non_avl_tree_list.insert(0, value)
        with set_recursion_limit(2 * size):  # Multiply by 2 just to make sure it's okay
            inserted_node = non_avl_tree_list.get(non_avl_tree_list.search(value) + 1)
        non_avl_depths_sum += inserted_node.depth()
    return (
        avl_operations / size,
        non_avl_operations / size,
        avl_depths_sum / size,
        non_avl_depths_sum / size,
    )


def create_balanced_tree_list(size: int) -> Tuple[float, float, float, float]:
    avl_tree_list, non_avl_tree_list = AVLTreeList(), BinarySearchTreeList()
    avl_operations, non_avl_operations = 0, 0
    avl_depths_sum, non_avl_depths_sum = 0, 0
    for i in range(1, size + 1):
        value = str(i)
        index = 2 * i - 2 ** math.floor(math.log2(2 * i))

        avl_operations += avl_tree_list.insert(index, value)
        inserted_node = avl_tree_list.get(avl_tree_list.search(value) + 1)
        avl_depths_sum += inserted_node.depth()

        non_avl_operations += non_avl_tree_list.insert(index, value)
        inserted_node = non_avl_tree_list.get(non_avl_tree_list.search(value) + 1)
        non_avl_depths_sum += inserted_node.depth()
    return (
        avl_operations / size,
        non_avl_operations / size,
        avl_depths_sum / size,
        non_avl_depths_sum / size,
    )


def create_random_tree_list(size: int) -> Tuple[float, float, float, float]:
    avl_tree_list, non_avl_tree_list = AVLTreeList(), BinarySearchTreeList()
    avl_operations, non_avl_operations = 0, 0
    avl_depths_sum, non_avl_depths_sum = 0, 0
    for i in range(size):
        value = str(i)
        avl_operations += insert_item_to_random_index_in_tree_list(avl_tree_list, value)
        inserted_node = avl_tree_list.get(avl_tree_list.search(value) + 1)
        avl_depths_sum += inserted_node.depth()

        non_avl_operations += insert_item_to_random_index_in_tree_list(
            non_avl_tree_list, value
        )
        inserted_node = non_avl_tree_list.get(non_avl_tree_list.search(value) + 1)
        non_avl_depths_sum += inserted_node.depth()
    return (
        avl_operations / size,
        non_avl_operations / size,
        avl_depths_sum / size,
        non_avl_depths_sum / size,
    )


def main():
    for i, size in enumerate(SIZES):
        # ---- 3.1 ----
        (
            avl_avg_operations,
            non_avl_avg_operations,
            avl_avg_depth,
            non_avl_avg_depth,
        ) = create_arithmetic_progressing_tree_list(size)
        print(
            f"{avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=arithmetic_avl)"
        )
        print(
            f"{non_avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=arithmetic_non_avl)"
        )
        print(
            f"{avl_avg_depth:.3f} average depth (size={size}, index={i + 1}, type=arithmetic_avl)"
        )
        print(
            f"{non_avl_avg_depth:.3f} average_depth done (size={size}, index={i + 1}, type=arithmetic_non_avl)"
        )

        # ---- 3.2 ----
        (
            avl_avg_operations,
            non_avl_avg_operations,
            avl_avg_depth,
            non_avl_avg_depth,
        ) = create_balanced_tree_list(size)
        print(
            f"{avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=balanced_avl)"
        )
        print(
            f"{non_avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=balanced_non_avl)"
        )
        print(
            f"{avl_avg_depth:.3f} average depth (size={size}, index={i + 1}, type=balanced_avl)"
        )
        print(
            f"{non_avl_avg_depth:.3f} average_depth done (size={size}, index={i + 1}, type=balanced_non_avl)"
        )

        # ---- 3.3 ----
        (
            avl_avg_operations,
            non_avl_avg_operations,
            avl_avg_depth,
            non_avl_avg_depth,
        ) = create_random_tree_list(size)
        print(
            f"{avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=random_avl)"
        )
        print(
            f"{non_avl_avg_operations:.3f} operations done (size={size}, index={i + 1}, type=random_non_avl)"
        )
        print(
            f"{avl_avg_depth:.3f} average depth (size={size}, index={i + 1}, type=random_avl)"
        )
        print(
            f"{non_avl_avg_depth:.3f} average_depth done (size={size}, index={i + 1}, type=random_non_avl)"
        )
        print()


if __name__ == "__main__":
    main()
