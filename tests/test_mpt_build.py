""" Tests the construction of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


from nose.tools import assert_equals

from mptpy.node import Node
from mptpy.mpt import MPT

import context


def test_mpt_from_file():
    """ Test if building from a file functions properly """
    mpt_obj = context.MPTS["test1"]
    assert_equals(mpt_obj.word.str_, "a bc c 0 1 a 2 e 2 3 d 4 5")
    assert_equals(mpt_obj.root.content, "a")

    root = Node(
        "a", Node(
            "bc", Node(
                "c", Node("0"), Node("1")), Node(
                "a", Node("2"), Node(
                    "e", Node("2"), Node("3")))), Node(
                        "d", Node("4"), Node("5")))
    mpt_obj.draw()
    assert_equals(root, mpt_obj.root)


def test_static_variables():
    """ Test the construction of mpts with multiple subtrees """
    mpt = context.MPTS["2htms"]
    assert_equals(
        str(mpt),
        "y0 y5 y8 Do 0 G1 0 1 Dn 3 G1 2 3 y6 Do 4 G2 4 5 y7 Dn 7 G2 6 7 Do 8 G3 8 9 y1 y4 Dn 11 G3 10 11 Do 12 G4 12 13 y2 Dn 15 G4 14 15 y3 Do 16 G5 16 17 Dn 19 G5 18 19"
    )


def test_mpt_from_word():
    """ Test if building from a word functions properly """
    mpt_obj = context.MPTS["test1"]

    mpt_obj2 = MPT("a bc c 0 1 a 2 e 2 3 d 4 5")

    assert_equals(mpt_obj, mpt_obj2)
