from datastructure_hw1_avl.theoretical_task.task_1_1 import create_random_tree_list
from datastructure_hw1_avl.theoretical_task.utils import delete_all_items_from_tree

SIZES = [1000 * 2 ** i for i in range(1, 11)]


def main():
    for i, size in enumerate(SIZES):
        insert_operations, avl_tree = create_random_tree_list(size)
        delete_operations = delete_all_items_from_tree(avl_tree)
        print(f"{delete_operations} operations done (size={size}, index={i + 1})")


if __name__ == "__main__":
    main()
