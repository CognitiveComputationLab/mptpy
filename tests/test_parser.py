""" Tests the parsing of MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
from nose.tools import assert_equals
from tests.context import mptpy

from mptpy.tools.parsing import BmptParser, Parser
from mptpy.mpt import MPT


MODEL_DIR = os.path.abspath("tests/test_models/test_build")
easy = Parser()
bmpt = BmptParser()


"""
def test_custom_leaves():
    mpt1 = BmptParser().parse(MODEL_DIR + "/testcustomleaves.txt")
    mpt2 = BmptParser().parse(MODEL_DIR + "/testBMPT.model")

    assert_equals(mpt1, mpt2)
"""


def test_easy_parsing():
    parser = Parser()
    mpt1 = parser.parse(MODEL_DIR + "/test1.model")
    assert_equals(str(mpt1), "a bc c 0 1 a 2 e 2 3 d 4 5")


def test_easy_parsing_w_joining():
    parser = Parser()
    mpt1 = parser.parse(MODEL_DIR + "/2htms_small.txt")
    print("Built one:: ")
    mpt1.draw()
    print()
    print("should be : ")
    mpt2 = MPT("y0 Do 0 G1 0 1 y1 Dn 3 G1 2 3 Do 4 G2 4 5")
    mpt2.draw()
    assert_equals(
        str(mpt1),
        "y0 Do 0 G1 0 1 y1 Dn 3 G1 2 3 Do 4 G2 4 5")  # maybe


def test_bmpt_parsing():
    parser = Parser()

    mpt = parser.parse(MODEL_DIR + "/testBMPT.model")
    assert_equals(str(mpt), "a b c 0 1 a 2 e 2 3 def 4 5")

    mpt = parser.parse(MODEL_DIR + "/testcustomleaves.txt")
    mpt.draw()
    assert_equals(str(mpt), "a b c albert ega a tante e tante 3 def 4 5")


def test_bmpt_parsing_w_joining():
    parser = Parser()
    mpt = parser.parse(MODEL_DIR + "/testBMPT2.model")
    assert_equals(str(mpt), "y0 a c 0 1 1 b 2 3")
