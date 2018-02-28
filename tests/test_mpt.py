""" Tests the functionalities of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.mpt import MPT

MODEL_DIR = "test_models/test_build/"


def test_equals():
    """ Test the equality testing of MPTs """
    mpt1 = MPT("a b c 1 2 a 4 e 4 5 d 6 7")
    mpt2 = MPT("pq b c 1 2 pq 4 e 4 5 z 6 7")
    mpt3 = MPT("a b c 1 2 a 4 e 4 5 6")

    assert_equals(mpt1, mpt2)
    assert_false(mpt1 == mpt3)
