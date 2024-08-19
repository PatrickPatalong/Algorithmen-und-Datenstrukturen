from time import time as current_time_in_seconds
import random

import pytest

from treap_solution import *

def test_for_repeat_mark():
    assert pytest.mark.repeat, "Please install 'pytest-repeat' [pip install pytest-repeat]."

# unbedingt repeat für randomisierte Algorithmen nehmen [pip install pytest-repeat]
@pytest.mark.repeat(100)
def test_random_treap():
    def check_treap_integrity(actual_treap, expected_priorities):
        _check_treap_properties(actual_treap)
        assert len(actual_treap) == len(expected_priorities)

        for key in expected_priorities.keys():
            assert _find_node(actual_treap, key)._priority == expected_priorities[key]

    # To reproduce error use the randseed
    randseed = int(current_time_in_seconds() * 1000000)
    random.seed(randseed)
    # print(f"\nCurrent seed: {randseed}")
    treap = RandomTreap()
    assert len(treap) == 0

    # Einfaches Einfügen
    priorities = dict()

    for i in range(1, 4):
        treap[i] = i * 10
        priorities[i] = _find_node(treap, i)._priority
        check_treap_integrity(treap, priorities)

    # Zugriff und Überschreiben eines Werts
    treap[1] = 11
    assert treap[1] == 11
    check_treap_integrity(treap, priorities)

    # Einfügen nach Überschreiben
    treap[0] = 0
    priorities[0] = _find_node(treap, 0)._priority
    check_treap_integrity(treap, priorities)

    # Mehrfacher Zugriff mit Überschreiben
    for i in range(10):
        treap[2] = i
    assert treap[2] == 9
    check_treap_integrity(treap, priorities)

    # Löschen
    del treap[2]
    del priorities[2]

    with pytest.raises(KeyError):
        _ = treap[2]

    assert _find_node(treap, 0)._value == 0
    assert _find_node(treap, 1)._value == 11
    assert _find_node(treap, 3)._value == 30

    check_treap_integrity(treap, priorities)


def test_dynamic_treap_insert_root():
    # setup
    treap = DynamicTreap()

    # preconditions
    assert len(treap) == 0
    with pytest.raises(KeyError):
        _ = treap["M"]

    # action
    treap["M"] = 1

    # postconditions
    node = _find_node(treap, "M")
    assert node is treap._root
    assert node._key == "M"
    assert node._value == 1
    assert node._priority == 1
    _check_children(node, None, None)


def test_dynamic_treap_insert_value_update():
    # setup
    treap = DynamicTreap()
    treap["M"] = 5
    node = _find_node(treap, "M")

    # preconditions
    assert len(treap) == 1
    assert node._value == 5

    # action
    treap["M"] = 1

    # postconditions
    assert len(treap) == 1
    assert node._value == 1


def test_dynamic_treap_insert_left():
    # setup
    treap = DynamicTreap()
    treap["B"] = None
    root_node = _find_node(treap, "B")

    # preconditions
    assert treap._root == root_node
    _check_treap_properties(treap)
    assert root_node._priority == 1

    # action
    # insert node in left subtree
    treap["A"] = None

    # postconditions
    assert treap._root == root_node
    _check_treap_properties(treap)
    assert root_node._priority == 1

    node = _find_node(treap, "A")
    _check_children(root_node, node, None)
    _check_children(node, None, None)
    assert node._priority == 1


def test_dynamic_treap_insert_right():
    # setup
    treap = DynamicTreap()
    treap["B"] = None
    root_node = _find_node(treap, "B")

    # preconditions
    assert treap._root == root_node
    _check_treap_properties(treap)
    assert root_node._priority == 1

    # action
    # insert node in left subtree
    treap["C"] = None

    # postconditions
    assert treap._root == root_node
    _check_treap_properties(treap)
    assert root_node._priority == 1

    node = _find_node(treap, "C")
    _check_children(root_node, None, node)
    _check_children(node, None, None)
    assert node._priority == 1


def test_dynamic_treap_priority_increment_root():
    # setup
    treap = DynamicTreap()
    treap["B"] = None
    old_root_node = _find_node(treap, "B")

    # preconditions
    assert treap._root == old_root_node
    _check_treap_properties(treap)
    _check_children(old_root_node, None, None)
    assert old_root_node._priority == 1

    # action
    _ = treap["B"]

    # postconditions
    new_root_node = _find_node(treap, "B")

    assert treap._root == new_root_node
    assert old_root_node is new_root_node

    _check_treap_properties(treap)
    _check_children(new_root_node, None, None)
    assert new_root_node._priority == 2


def test_dynamic_treap_priority_increment_left_child():
    # setup
    treap = DynamicTreap()
    treap["B"] = None
    treap["A"] = None
    old_root_node = _find_node(treap, "B")
    old_left_child = _find_node(treap, "A")

    # preconditions
    assert treap._root == old_root_node
    _check_treap_properties(treap)
    _check_children(old_root_node, old_left_child, None)
    _check_children(old_left_child, None, None)
    assert old_root_node._priority == 1
    assert old_left_child._priority == 1

    # action
    _ = treap["A"]

    # postconditions
    new_root_node = _find_node(treap, "A")
    right_child = _find_node(treap, "B")

    assert treap._root == new_root_node
    assert old_left_child is new_root_node
    assert old_root_node is right_child

    _check_treap_properties(treap)
    _check_children(new_root_node, None, right_child)
    _check_children(right_child, None, None)
    assert new_root_node._priority == 2
    assert right_child._priority == 1


def test_dynamic_treap_priority_increment_right_child():
    # setup
    treap = DynamicTreap()
    treap["B"] = None
    treap["C"] = None
    old_root_node = _find_node(treap, "B")
    old_right_child = _find_node(treap, "C")

    # preconditions
    assert treap._root == old_root_node
    _check_treap_properties(treap)
    _check_children(old_root_node, None, old_right_child)
    _check_children(old_right_child, None, None)
    assert old_root_node._priority == 1
    assert old_right_child._priority == 1

    # action
    _ = treap["C"]

    # postconditions
    new_root_node = _find_node(treap, "C")
    left_child = _find_node(treap, "B")

    assert treap._root == new_root_node
    assert old_right_child is new_root_node
    assert old_root_node is left_child

    _check_treap_properties(treap)
    _check_children(new_root_node, left_child, None)
    _check_children(left_child, None, None)
    assert new_root_node._priority == 2
    assert left_child._priority == 1


def test_dynamic_treap_delete_leaf():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["C"], None, nodes["G"])
        _check_children(nodes["G"], nodes["F"], nodes["M"])
        _check_children(nodes["F"], nodes["E"], None)
        _check_children(nodes["E"], None, None)
        _check_children(nodes["M"], None, nodes["N"])
        _check_children(nodes["N"], None, None)

    _test_dynamic_treap_remove_key("A", explicit_tree_structure_check)


def _test_dynamic_treap_remove_key(key_to_remove, explicit_tree_structure_check=lambda nodes: None):
    # setup
    treap = DynamicTreap()
    keys = ("C", "A", "G", "F", "E", "M", "N")
    for key in keys:
        treap[key] = None

    #              C (8)
    #       /              \
    #     A (4)           G (6)
    #    /    \         /       \
    #                F (3)     M (5)
    #               /    \    /    \
    #           E (2)             L (3)

    target_priorities = {"C": 8, "A": 4, "G": 6, "F": 3, "E": 2, "M": 5, "N": 3}
    for key, value in target_priorities.items():
        _find_node(treap, key)._priority = value

    # preconditions
    for key, value in target_priorities.items():
        assert _find_node(treap, key)._priority == value

    # remove root
    del treap[key_to_remove]

    # postconditions
    for key, value in target_priorities.items():
        if key == key_to_remove:
            with pytest.raises(KeyError):
                _ = treap[key_to_remove]
        else:
            assert _find_node(treap, key)._priority == value
    # gray box test
    explicit_tree_structure_check({key: _find_node(treap, key) for key in keys if key != key_to_remove})


def test_dynamic_treap_delete_branch_with_right_child():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["C"], nodes["A"], nodes["G"])
        _check_children(nodes["A"], None, None)
        _check_children(nodes["G"], nodes["F"], nodes["N"])
        _check_children(nodes["F"], nodes["E"], None)
        _check_children(nodes["E"], None, None)
        _check_children(nodes["N"], None, None)

    _test_dynamic_treap_remove_key("M", explicit_tree_structure_check)


def test_dynamic_treap_delete_branch_with_left_child():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["C"], nodes["A"], nodes["G"])
        _check_children(nodes["A"], None, None)
        _check_children(nodes["G"], nodes["E"], nodes["M"])
        _check_children(nodes["E"], None, None)
        _check_children(nodes["M"], None, nodes["N"])
        _check_children(nodes["N"], None, None)

    _test_dynamic_treap_remove_key("F", explicit_tree_structure_check)


def test_dynamic_treap_delete_root():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["G"], nodes["A"], nodes["M"])
        _check_children(nodes["A"], None, nodes["F"])
        _check_children(nodes["F"], nodes["E"], None)
        _check_children(nodes["E"], None, None)
        _check_children(nodes["M"], None, nodes["N"])
        _check_children(nodes["N"], None, None)

    _test_dynamic_treap_remove_key("C", explicit_tree_structure_check)


def test_dynamic_treap_find_none():
    treap = DynamicTreap()

    # preconditions
    assert treap._root is None
    assert len(treap) == 0

    # action
    with pytest.raises(KeyError):
        _ = treap["M"]

    # postconditions
    assert treap._root is None
    assert len(treap) == 0


def test_dynamic_treap_find_root():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["D"], nodes["B"], nodes["F"])
        _check_children(nodes["B"], nodes["A"], nodes["C"])
        _check_children(nodes["A"], None, None)
        _check_children(nodes["C"], None, None)
        _check_children(nodes["F"], nodes["E"], nodes["G"])
        _check_children(nodes["E"], None, None)
        _check_children(nodes["G"], None, None)

    _test_dynamic_treap_find_key("D", explicit_tree_structure_check)


def _test_dynamic_treap_find_key(key_to_find, explicit_tree_structure_check=lambda nodes: None):
    # setup
    treap = DynamicTreap()
    keys = ["D", "B", "A", "C", "F", "E", "G"]
    for key in keys:
        treap[key] = None
    #                D (1)
    #          /              \
    #        B (1)           F (1)
    #      /      \         /     \
    #    A (1)   C (1)   E (1)   G (1)
    #    |   |   |   |   |   |   |   |
    #
    nodes = {key: _find_node(treap, key) for key in keys}

    # preconditions
    _check_treap_properties(treap)
    for node in nodes.values():
        assert node._priority == 1

    # action
    # find node in left subtree
    _ = treap[key_to_find]

    # postconditions
    _check_treap_properties(treap)
    for key in keys:
        if key == key_to_find:
            assert nodes[key]._priority == 2
        else:
            assert nodes[key]._priority == 1
    # gray box test
    explicit_tree_structure_check(nodes)


def test_dynamic_treap_find_left():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["B"], nodes["A"], nodes["D"])
        _check_children(nodes["A"], None, None)
        _check_children(nodes["D"], nodes["C"], nodes["F"])
        _check_children(nodes["C"], None, None)
        _check_children(nodes["F"], nodes["E"], nodes["G"])
        _check_children(nodes["E"], None, None)
        _check_children(nodes["G"], None, None)

    _test_dynamic_treap_find_key("B", explicit_tree_structure_check)


def test_dynamic_treap_find_right():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["F"], nodes["D"], nodes["G"])
        _check_children(nodes["D"], nodes["B"], nodes["E"])
        _check_children(nodes["B"], nodes["A"], nodes["C"])
        _check_children(nodes["A"], None, None)
        _check_children(nodes["C"], None, None)
        _check_children(nodes["E"], None, None)
        _check_children(nodes["G"], None, None)

    _test_dynamic_treap_find_key("F", explicit_tree_structure_check)


def test_dynamic_treap_find_leaf():
    def explicit_tree_structure_check(nodes):
        _check_children(nodes["C"], nodes["B"], nodes["D"])
        _check_children(nodes["B"], nodes["A"], None)
        _check_children(nodes["A"], None, None)
        _check_children(nodes["D"], None, nodes["F"])
        _check_children(nodes["F"], nodes["E"], nodes["G"])
        _check_children(nodes["E"], None, None)
        _check_children(nodes["G"], None, None)

    _test_dynamic_treap_find_key("C", explicit_tree_structure_check)


def _check_children(node, left_child, right_child):
    # use is because it is the same object
    assert node._left is left_child and node._right is right_child


def _check_treap_properties(treap):
    _check_key_sorted(treap._root)
    _check_priority_sorted(treap._root)


def _check_key_sorted(node):
    if node._left is not None:
        _check_key_sorted(node._left)
        assert node._key > node._left._key

    if node._right is not None:
        _check_key_sorted(node._right)
        assert node._key < node._right._key


def _check_priority_sorted(node):
    if node._left is not None:
        _check_priority_sorted(node._left)
        assert node._priority >= node._left._priority

    if node._right is not None:
        _check_priority_sorted(node._right)
        assert node._priority >= node._right._priority


def _find_node(tree, key):
    node = tree._root
    while True:
        if node is None:
            raise KeyError(key)

        if key == node._key:
            return node
        elif key < node._key:
            node = node._left
        else:
            node = node._right


if __name__ == "__main__":
    pytest.main()
