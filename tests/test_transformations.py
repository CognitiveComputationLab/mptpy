""" Tests the transformations from trees to words and vice versa.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.tools import transformations
from mptpy.node import Node


def test_tree_to_word():
    root = Node("a", Node("b", Node("1", leaf=True), Node("2", leaf=True)), Node("3", leaf=True))
    assert_equals(transformations.tree_to_word(root), "a b 1 2 3")

    root = Node("a", Node("bef", Node("a", Node("6", leaf=True), Node("8", leaf=True)), Node("2", leaf=True)), Node("13", leaf=True))
    assert_equals(transformations.tree_to_word(root), "a bef a 6 8 2 13")


def test_word_to_tree():
    pass