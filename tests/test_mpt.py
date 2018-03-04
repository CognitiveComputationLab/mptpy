""" Tests the functionalities of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.mpt import MPT, build_from_file

MODEL_DIR = "tests/test_models/test_build"


def test_equals():
    """ Test the equality testing of MPTs """
    mpt1 = MPT("a b c 1 2 a 4 e 4 5 d 6 7")
    mpt2 = MPT("pq b c 1 2 pq 4 e 4 5 z 6 7")
    mpt3 = MPT("a b c 1 2 a 4 e 4 5 6")

    assert_equals(mpt1, mpt2)
    assert_false(mpt1 == mpt3)
    assert_false(mpt1 != mpt2)


def test_to_easy():
    """ Test the translation to the easy format """
    mpt = build_from_file(MODEL_DIR + "/test1.model")
    easy = mpt.to_easy()
    print(easy)
    assert_equals(easy, "a * bc * c\na * bc * (1-c)\na * (1-bc) * a + a * (1-bc) * (1-a) * e\na * (1-bc) * (1-a) * (1-e)\n(1-a) * d\n(1-a) * (1-d)\n")

def test_save():
    mpt = build_from_file(MODEL_DIR + "/test1.model")
    mpt.save(MODEL_DIR + "/testsave.model")

    mpt.save(MODEL_DIR + "/testsavebmpt.model", form="BMPT")


def test_branch_formulae():
    leaf = lambda x: all([ch in string.ascii_uppercase for ch in x])
    mpt1 = MPT('p A B', is_leaf=leaf)

    assert_equals(mpt1.get_formulae(), (['p', '(1 - p)'], ['A', 'B']))

    mpt2 = MPT('r N g N O', is_leaf=leaf)
    assert_equals(mpt2.get_formulae(), (['r', '(1 - r) * g', '(1 - r) * (1 - g)'], ['N', 'N', 'O']))