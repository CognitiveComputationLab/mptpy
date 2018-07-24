""" Tests the functionalities of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.mpt import MPT
from mptpy.properties import property
from mptpy.tools.parsing import Parser
from mptpy.tools.transformations import to_easy

parser = Parser()

MODEL_DIR = "tests/test_models/test_build"


def test_equals():
    """ Test the equality testing of MPTs """
    mpt1 = MPT("a b c 1 2 a 4 e 4 5 d 6 7")
    mpt2 = MPT("pq b c 1 2 pq 4 e 4 5 z 6 7")
    mpt3 = MPT("a b c 1 2 a 4 e 4 5 6")
    mpt4 = MPT("pq b c 1 2 pq 4 e 4 5 d 6 8")

    assert_equals(mpt1, mpt2)
    assert_false(mpt1 == mpt3)
    assert_false(mpt1 != mpt2)
    assert_false(mpt4 == mpt1)


def test_tree_length():
    """ Test the tree length function """
    mpt = MPT("pq b c 1 2 pq 4 e 4 5 z 6 7")
    assert_equals(len(mpt.root), 13)
    assert_equals(len(mpt.root.neg), 3)
    assert_equals(len(mpt.root.pos), 9)


def test_to_easy():
    """ Test the translation to the easy format """
    mpt = parser.parse(MODEL_DIR + "/test1.model")
    easy = to_easy(mpt)
    print(easy)
    assert_equals(
        easy,
        "a * bc * c\na * bc * (1-c)\na * (1-bc) * a + a * (1-bc) * (1-a) * e\na * (1-bc) * (1-a) * (1-e)\n(1-a) * d\n(1-a) * (1-d)\n")


def test_save():
    mpt = parser.parse(MODEL_DIR + "/test1.model")
    mpt.save(MODEL_DIR + "/testsave.model")

    mpt.save(MODEL_DIR + "/testsavebmpt.model", form="BMPT")


def test_get_levels():
    s = "b c 2 1 a 2 d 1 0"

    mpt = MPT(s)

    levels = mpt.get_levels(mpt.root)
    levels = {key: [node.content for node in value]
              for key, value in levels.items()}
    print(levels)
    assert_equals({0: ["b"], 1: ["c", "a"], 2: [
                  "2", "1", "2", "d"], 3: ["1", "0"]}, levels)


def test_identifiable():
    mpt = parser.parse(MODEL_DIR + "/test1.model")
    ident = property.check(mpt, "identifiable")
    assert_equals(ident, True)
