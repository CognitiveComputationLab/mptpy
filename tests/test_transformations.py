""" Tests the transformations from trees to words and vice versa.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.tools import transformations, parsing
from mptpy.node import Node
from mptpy.mpt_word import MPTWord
from mptpy.mpt import MPT


def test_tree_to_word():
    """ Test the transformation from a tree (root node) to a word """
    root = Node("a", Node("b", Node("1"), Node("2")), Node("3"))
    assert_equals(str(MPT(root)), "a b 1 2 3")

    root = Node("a", Node("bef", Node("a", Node("6"), Node("8")), Node("2")), Node("13"))
    assert_equals(str(MPT(root)), "a bef a 6 8 2 13")


def test_word_to_tree():
    """ Test the transformation from a word to a tree (root node) """
    root = Node("a", Node("bef", Node("a", Node("6"), Node("8")), Node("2")), Node("13"))
    root2 = transformations.word_to_nodes(MPTWord("a bef a 6 8 2 13"))

    assert_equals(MPT(root), MPT(root2))

    parser = parsing.EasyParser()
    mpt = parser.parse("tests/test_models/test_build/2htms.txt")

    word = MPTWord(
        "y0 y5 y8 Do 0 G1 0 1 Dn 3 G1 2 3 y6 Do 4 G2 4 5 y7 Dn 7 G2 6 7 Do 8 G3 8 9 y1 y4 Dn 11 G3 10 11 Do 12 G4 12 13 y2 Dn 15 G4 14 15 y3 Do 16 G5 16 17 Dn 19 G5 18 19"
    )
    mpt2 = MPT(transformations.word_to_nodes(word))
    print(type(mpt))
    print(type(mpt2))
    assert_equals(mpt, mpt2)
