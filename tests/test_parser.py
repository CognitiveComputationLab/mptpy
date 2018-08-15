""" Tests the parsing of MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
from nose.tools import assert_equals

from mptpy.mpt import MPT

import context



def test_parsing_w_joining():
    """ Tests if joining subtrees works """
    mpt1 = context.MPTS["2htms_small"]
    mpt2 = MPT("y0 Do 0 G1 0 1 y1 Dn 3 G1 2 3 Do 4 G2 4 5")
    assert_equals(
        str(mpt1),
        "y0 Do 0 G1 0 1 y1 Dn 3 G1 2 3 Do 4 G2 4 5")


def test_bmpt_parsing():
    """ Tests the BMPT parser """
    mpt = context.MPTS["testBMPT"]
    assert_equals(str(mpt), "a b c 0 1 a 2 e 2 3 def 4 5")

    mpt = context.MPTS["testcustomleaves"]
    mpt.draw()
    assert_equals(str(mpt), "a b c albert ega a tante e tante 3 def 4 5")


def test_bmpt_parsing_w_joining():
    """ tests the bmpt parser with joining trees """
    mpt = context.MPTS["testBMPT2"]
    assert_equals(str(mpt), "y0 a c 0 1 1 b 2 3")
