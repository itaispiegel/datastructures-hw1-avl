from datastructure_hw1_avl.theoretical_task.task_1_1 import create_random_tree_list
from datastructure_hw1_avl.theoretical_task.utils import insert_and_remove_items

SIZES = [1000 * 2 ** i for i in range(1, 11)]


def main():
    for i, size in enumerate(SIZES):
        insert_operations, tree_list = create_random_tree_list(size // 2)
        operations = insert_and_remove_items(tree_list, size // 4)
        print(f"{operations} operations done (size={size}, index={i + 1})")


if __name__ == "__main__":
    main()
