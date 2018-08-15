""" Tests the transformations from trees to words and vice versa.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals

from mptpy.visualization import visualize_mpt
from mptpy.mpt import MPT

import context


def test_to_tikz():
    """ Test the conversion to tikz """
    tikz_str = r"\Tree [.a 13 [.ce [.e 5 6 ] 0 ] ]"

    mpt = MPT("a 13 ce e 5 6 0")

    assert_equals(visualize_mpt.to_tikz(mpt), tikz_str)
