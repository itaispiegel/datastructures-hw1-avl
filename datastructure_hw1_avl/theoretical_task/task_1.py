from datastructure_hw1_avl.theoretical_task.utils import (
    create_random_tree_list,
    delete_all_items_from_tree,
    insert_and_remove_items_randomly,
)

SIZES = [1000 * 2 ** i for i in range(1, 11)]


def task__1_1():
    print("-----Task 1.1-----")
    for i, size in enumerate(SIZES):
        operations, avl_tree = create_random_tree_list(size)
        print(f"{operations} operations done (size={size}, index={i + 1})")
    print()


def task__1_2():
    print("-----Task 1.2-----")
    for i, size in enumerate(SIZES):
        insert_operations, avl_tree = create_random_tree_list(size)
        delete_operations = delete_all_items_from_tree(avl_tree)
        print(f"{delete_operations} operations done (size={size}, index={i + 1})")
    print()


def task__1_3():
    print("-----Task 1.3-----")
    for i, size in enumerate(SIZES):
        insert_operations, tree_list = create_random_tree_list(size // 2)
        operations = insert_and_remove_items_randomly(tree_list, size // 4)
        print(f"{operations} operations done (size={size}, index={i + 1})")
    print()


def main():
    task__1_1()
    task__1_2()
    task__1_3()


if __name__ == "__main__":
    main()
