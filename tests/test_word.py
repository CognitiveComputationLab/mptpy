""" Tests the functionalities of words in the BMPT language.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals, assert_false
from tests.context import mptpy
from mptpy.mpt_word import MPTWord

def test_abstract():
    """ Test the abstract formulation of MPT strings """
    mpt1 = MPTWord("a b c 1 2 a 4 e 4 5 d 6 7")
    mpt2 = MPTWord("pq b c 1 2 pq 4 e 4 5 z 6 7")
    mpt3 = MPTWord("a b c 1 2 a 4 e 4 5 6")

    assert_equals(mpt1.abstract(), "p0 p1 p2 a0 a1 p0 a2 p3 a2 a3 p4 a4 a5")
    assert_equals(mpt2.abstract(), "p0 p1 p2 a0 a1 p0 a2 p3 a2 a3 p4 a4 a5")
    assert_equals(mpt3.abstract(), "p0 p1 p2 a0 a1 p0 a2 p3 a2 a3 a4")

def test_get_answers():
    """ Test if returning all the leaf node contents works """
    mpt2 = MPTWord("pq b c 1 2 pq 4 e 4 5 z 6 7")
    assert_equals(mpt2.answers, ["1", "2", "4", "4", "5", "6", "7"])

def test_get_parameters():
    """ Test if returning all the parameters works """
    mpt2 = MPTWord("pq b c 1 2 pq 4 e 4 5 z 6 7")
    assert_equals(mpt2.parameters, ["pq", "b", "c", "pq", "e", "z"])

def test_is_leaf():
    """ Test if judging nodes to be leaves or not works """
    mpt3 = MPTWord("a b c 1 2 a 4 e 4 5 6")
    assert_equals(True, mpt3.is_leaf("3"))
    assert_equals(True, mpt3.is_leaf("13"))
    assert_equals(False, mpt3.is_leaf("p3"))
    assert_equals(False, mpt3.is_leaf("pq"))

def test_split():
    word1 = MPTWord("p A B")
    assert_equals(word1.split(), ('A', 'B'))
    word2 = MPTWord('a N b N O')
    assert_equals(word2.split(), ('N', 'b N O'))
    word3 = MPTWord('a b N O N')
    assert_equals(word3.split(), ('b N O', 'N'))

