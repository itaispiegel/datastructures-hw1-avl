import random
import statistics
from typing import Tuple

from datastructure_hw1_avl.avl import AVLTreeList

random.seed(100)
SIZES = [1000 * 2 ** i for i in range(1, 11)]


class AVLTreeListWithSpecialSplit(AVLTreeList):
    def split(self, index: int) -> Tuple[int, int]:
        node = self.get(index + 1)

        small_tree = AVLTreeList(node.left, remove_parent_from_root=True)
        large_tree = AVLTreeList(node.right, remove_parent_from_root=True)

        nodes_list, sides_list, joins_costs = [], [], []
        while node.parent is not None:
            nodes_list.append(node.parent)
            sides_list.append(node.isParentRight())
            node = node.parent

        for i, node in enumerate(nodes_list):
            node.parent = None
            if sides_list[i]:
                cost = large_tree.join_with_axis(
                    AVLTreeList(node.right, remove_parent_from_root=True), node
                )
            else:
                temp_tree = AVLTreeList(node.left, remove_parent_from_root=True)
                cost = temp_tree.join_with_axis(small_tree, node)
                small_tree = temp_tree
            joins_costs.append(cost)

        return max(joins_costs), statistics.mean(joins_costs)


def create_two_random_tree_lists(
    size: int,
) -> Tuple[AVLTreeListWithSpecialSplit, AVLTreeListWithSpecialSplit]:
    tree_list1, tree_list2 = (
        AVLTreeListWithSpecialSplit(),
        AVLTreeListWithSpecialSplit(),
    )
    for i in range(size):
        index = random.randint(0, tree_list1.length())
        value = str(i)
        tree_list1.insert(index, value)
        tree_list2.insert(index, value)
    return tree_list1, tree_list2


def main():
    for i, size in enumerate(SIZES):
        tree_list1, tree_list2 = create_two_random_tree_lists(size)
        random_index = random.randint(0, tree_list1.length())
        max_cost_random_index, avg_cost_random_index = tree_list1.split(random_index)
        print(
            f"max_cost_random_index={max_cost_random_index}, "
            f"avg_cost_random_index={avg_cost_random_index:.3f}, "
            f"i={i + 1}, "
            f"size={size}"
        )

        root_predecessor_index = tree_list2.root.left.rank - 1
        max_cost_root_pred, avg_cost_root_pred = tree_list2.split(
            root_predecessor_index
        )
        print(
            f"max_cost_root_pred={max_cost_root_pred}, "
            f"avg_cost_root_pred={avg_cost_root_pred:.3f}, "
            f"i={i + 1}, "
            f"size={size}"
        )
        print()


if __name__ == "__main__":
    main()
