""" Tests the construction of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


from nose.tools import assert_equals
from tests.context import mptpy
from mptpy.node import Node


MODEL_DIR = "tests/test_models/test_build/"


def test_mpt_from_file():
    """ Test if building from a file functions properly """
    file_path = MODEL_DIR + "test1.model"
    mpt_obj = mptpy.mpt.build_from_file(file_path)
    assert_equals(mpt_obj.word.word, "a b c 0 1 a 2 e 2 3 d 4 5")
    assert_equals(mpt_obj.root.content, "a")

    root = Node("a", Node("b", Node("c", Node("0", leaf=True), Node("1", leaf=True)), Node("a", Node("2"), Node("e", Node("2", leaf=True), Node("3", leaf=True)))), Node("d", Node("4", leaf=True), Node("5", leaf=True)))
    assert_equals(root, mpt_obj.root)


def test_mpt_from_word():
    """ Test if building from a word functions properly """
    file_path = MODEL_DIR + "test1.model"
    mpt_obj = mptpy.mpt.build_from_file(file_path)

    mpt_obj2 = mptpy.mpt.MPT("a b c 0 1 a 2 e 2 3 d 4 5")

    assert_equals(mpt_obj, mpt_obj2)
