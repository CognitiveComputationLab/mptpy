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
    assert_equals(mpt_obj.word.str_, "a bc c 0 1 a 2 e 2 3 d 4 5")
    assert_equals(mpt_obj.root.content, "a")

    root = Node("a", Node("bc", Node("c", Node("0", leaf=True), Node("1", leaf=True)), Node("a", Node("2"), Node("e", Node("2", leaf=True), Node("3", leaf=True)))), Node("d", Node("4", leaf=True), Node("5", leaf=True)))
    mpt_obj.draw()
    assert_equals(root, mpt_obj.root)


def test_static_variables():
    """ Test the construction of mpts with multiple subtrees """
    mpt = mptpy.mpt.build_from_file(MODEL_DIR + "2htms.txt")

    assert_equals(
        mpt.string,
        "y0 y5 y8 Do 0 G1 0 1 Dn 3 G1 2 3 y6 Do 4 G2 4 5 y7 Dn 7 G2 6 7 Do 8 G3 8 9 y1 y4 Dn 11 G3 10 11 Do 12 G4 12 13 y2 Dn 15 G4 14 15 y3 Do 16 G5 16 17 Dn 19 G5 18 19"
    )


def test_mpt_from_word():
    """ Test if building from a word functions properly """
    file_path = MODEL_DIR + "test1.model"
    mpt_obj = mptpy.mpt.build_from_file(file_path)

    mpt_obj2 = mptpy.mpt.MPT("a bc c 0 1 a 2 e 2 3 d 4 5")
    mpt_obj2.draw()

    assert_equals(mpt_obj, mpt_obj2)
