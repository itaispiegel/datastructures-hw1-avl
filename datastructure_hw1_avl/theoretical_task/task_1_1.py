from datastructure_hw1_avl.theoretical_task.utils import create_random_tree_list

SIZES = [1000 * 2 ** i for i in range(1, 11)]


def main():
    for i, size in enumerate(SIZES):
        operations, avl_tree = create_random_tree_list(size)
        print(f"{operations} operations done (size={size}, index={i + 1})")


if __name__ == "__main__":
    main()
