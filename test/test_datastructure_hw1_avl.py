import pytest

from datastructure_hw1_avl.avl import AVLTreeList


@pytest.fixture
def empty_tree():
    return AVLTreeList()


@pytest.fixture
def non_empty_tree():
    tree = AVLTreeList()
    tree.insert(0, "a")
    tree.insert(1, "b")
    tree.insert(2, "c")
    tree.insert(3, "d")
    return tree


def test_empty_tree_root_is_virtual(empty_tree: AVLTreeList):
    assert empty_tree.root.isVirtualNode()


def test_inserting_item_to_tree_marks_the_root_as_real(empty_tree: AVLTreeList):
    empty_tree.insert(1, "a")
    assert empty_tree.root.isVirtualNode()


def test_insert_item_at_too_large_index_returns_negative_one(empty_tree: AVLTreeList):
    assert empty_tree.insert(11, "a") == -1
    assert empty_tree.empty()


def test_retrieve_items(non_empty_tree: AVLTreeList):
    assert non_empty_tree.retrieve(0) == "a"
    assert non_empty_tree.retrieve(1) == "b"
    assert non_empty_tree.retrieve(2) == "c"
    assert non_empty_tree.retrieve(3) == "d"


def test_insert_item_in_the_middle(non_empty_tree: AVLTreeList):
    non_empty_tree.insert(1, "new_item")
    assert non_empty_tree.retrieve(0) == "a"
    assert non_empty_tree.retrieve(1) == "new_item"
    assert non_empty_tree.retrieve(2) == "b"
    assert non_empty_tree.retrieve(3) == "c"
    assert non_empty_tree.retrieve(4) == "d"


@pytest.mark.parametrize(("index",), [[0], [-1], [2]])
def test_get_item_when_index_is_out_bounds_raises_exception(
    empty_tree: AVLTreeList, index: int
):
    empty_tree.insert(0, "a")
    with pytest.raises(IndexError, match="out of range"):
        assert empty_tree.get(index)


def test_retrieve_items_after_delete(non_empty_tree: AVLTreeList):
    non_empty_tree.delete(2)

    assert non_empty_tree.retrieve(0) == "a"
    assert non_empty_tree.retrieve(1) == "b"
    assert non_empty_tree.retrieve(2) == "d"


def test_get_first_and_last(empty_tree: AVLTreeList):
    assert empty_tree.first() is None
    assert empty_tree.last() is None

    empty_tree.insert(0, "a")
    assert empty_tree.first() == empty_tree.last() == "a"

    empty_tree.insert(1, "b")
    assert empty_tree.first() == "a" and empty_tree.last() == "b"

    empty_tree.insert(0, "c")
    assert empty_tree.first() == "c" and empty_tree.last() == "b"


def test_get_first_and_last_after_deleting_first(non_empty_tree: AVLTreeList):
    non_empty_tree.delete(0)
    assert non_empty_tree.first() == "b"

    non_empty_tree.delete(2)
    assert non_empty_tree.last() == "c"


def test_list_to_array_for_empty_list(empty_tree: AVLTreeList):
    array = empty_tree.listToArray()
    assert array == []


def test_list_to_array_for_non_empty_list(non_empty_tree: AVLTreeList):
    array = non_empty_tree.listToArray()
    assert array == ["a", "b", "c", "d"]
