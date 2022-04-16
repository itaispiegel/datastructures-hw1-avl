from test.conftest import LARGE_TREE_SIZE

import pytest

from datastructure_hw1_avl.avl import AVLTreeList


def test_empty_tree_root_is_virtual(empty_tree: AVLTreeList):
    assert empty_tree.root.isVirtualNode()


def test_inserting_item_to_tree_marks_the_root_as_real(empty_tree: AVLTreeList):
    empty_tree.insert(1, "a")
    assert empty_tree.root.isVirtualNode()


def test_insert_item_at_too_large_index_returns_negative_one(empty_tree: AVLTreeList):
    assert empty_tree.insert(11, "a") == 0
    assert empty_tree.empty()


def test_retrieve_items_from_large_tree(large_tree: AVLTreeList):
    for i in range(LARGE_TREE_SIZE):
        assert large_tree.retrieve(i) == str(i)


def test_insert_item_in_the_middle_of_the_small_tree(small_tree: AVLTreeList):
    small_tree.insert(1, "new_item")
    assert small_tree.retrieve(0) == "a"
    assert small_tree.retrieve(1) == "new_item"
    assert small_tree.retrieve(2) == "b"
    assert small_tree.retrieve(3) == "c"
    assert small_tree.retrieve(4) == "d"


def test_insert_item_in_the_middle_of_the_large_tree(large_tree: AVLTreeList):
    large_tree.insert(420, "new_item")
    for i in range(420):
        assert large_tree.retrieve(i) == str(i)
    assert large_tree.retrieve(420) == "new_item"
    for i in range(421, LARGE_TREE_SIZE + 1):
        assert large_tree.retrieve(i) == str(i - 1)


@pytest.mark.parametrize(("index",), [[0], [-1], [2]])
def test_get_item_when_index_is_out_bounds_raises_exception(
    empty_tree: AVLTreeList, index: int
):
    empty_tree.insert(0, "a")
    with pytest.raises(IndexError, match="out of range"):
        assert empty_tree.get(index)


def test_retrieve_items_after_delete_from_small_tree(small_tree: AVLTreeList):
    small_tree.delete(2)

    assert small_tree.retrieve(0) == "a"
    assert small_tree.retrieve(1) == "b"
    assert small_tree.retrieve(2) == "d"


def test_retrieve_items_after_delete_from_large_tree(large_tree: AVLTreeList):
    large_tree.delete(278)

    assert large_tree.length() == LARGE_TREE_SIZE - 1
    for i in range(278):
        assert large_tree.retrieve(i) == str(i)
    for i in range(278, LARGE_TREE_SIZE - 1):
        assert large_tree.retrieve(i) == str(i + 1)


def test_delete_when_there_is_only_a_leaf_node(empty_tree: AVLTreeList):
    empty_tree.insert(0, "a")
    assert empty_tree.retrieve(0) == "a"
    empty_tree.delete(0)
    assert empty_tree.empty()
    empty_tree.insert(0, "b")
    assert empty_tree.retrieve(0) == "b"


def test_get_first_and_last_on_empty_tree(empty_tree: AVLTreeList):
    assert empty_tree.first() is None
    assert empty_tree.last() is None

    empty_tree.insert(0, "a")
    assert empty_tree.first() == empty_tree.last() == "a"

    empty_tree.insert(1, "b")
    assert empty_tree.first() == "a" and empty_tree.last() == "b"

    empty_tree.insert(0, "c")
    assert empty_tree.first() == "c" and empty_tree.last() == "b"


def test_get_first_and_last_after_deleting_first(small_tree: AVLTreeList):
    small_tree.delete(0)
    assert small_tree.first() == "b"

    small_tree.delete(2)
    assert small_tree.last() == "c"


def test_list_to_array_for_empty_list(empty_tree: AVLTreeList):
    array = empty_tree.listToArray()
    assert array == []


def test_list_to_array_for_non_empty_list(small_tree: AVLTreeList):
    array = small_tree.listToArray()
    assert array == ["a", "b", "c", "d"]


def test_concat_two_trees_for_non_empty_tree(small_tree: AVLTreeList):
    tree2 = AVLTreeList()
    tree2.insert(0, "e")
    tree2.insert(1, "f")
    tree2.insert(2, "g")
    tree2.insert(3, "h")
    small_tree.concat(tree2)

    expected_tree = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(small_tree.length()):
        assert small_tree.retrieve(i) == expected_tree[i]

    assert small_tree.last() == "h"
    assert small_tree.retrieve(3) == "d"
    assert small_tree.retrieve(5) == "f"
    assert small_tree.root.parent is None
    assert small_tree.root.value == "f"


def test_split_large_tree(large_tree: AVLTreeList):
    array = large_tree.listToArray()
    index = 120
    result = large_tree.split(index)
    assert result[0].listToArray() == array[0:index]
    assert result[1] == array[index]
    assert result[2].listToArray() == array[index + 1 :]


def test_concat_with_empty_list_does_not_change_first_and_last(large_tree: AVLTreeList, empty_tree: AVLTreeList):
    first, last = large_tree.first(), large_tree.last()
    large_tree.concat(empty_tree)
    assert large_tree.first() == first
    assert large_tree.last() == last


def test_concat_when_current_list_is_empty(empty_tree: AVLTreeList, small_tree: AVLTreeList):
    first, last = small_tree.first(), small_tree.last()
    empty_tree.concat(small_tree)
    assert empty_tree.first() == first
    assert empty_tree.last() == last


def test_concat_with_singleton_list_changes_only_last_item(large_tree: AVLTreeList):
    val = "NEW_ITEM"
    singleton_list = AVLTreeList()
    singleton_list.insert(0, val)

    first = large_tree.first()
    large_tree.concat(singleton_list)
    assert large_tree.first() == first
    assert large_tree.last() == val
