""" Tests the operations on MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from itertools import compress

from nose.tools import assert_equals

from mptpy.mpt import MPT
from mptpy.optimization.operations.deletion import Deletion
import mptpy.optimization.operations.substitution as sub
import context


MPTdeletion = context.MPTS["testdeletion"]


def test_deletion():
    """
            b
      c           a
    2   1       2   d
                   1  0
    """
    

    deletion = Deletion(MPTdeletion)
    candidates = deletion.generate_candidates()

    assert_equals(sorted(candidates),
                  sorted([str(MPTdeletion),
                          "b c 2 1 a 2 0",
                          "b c 2 1 d 1 0",
                          "b c 2 1 0",
                          "b 2 a 2 d 1 0",
                          "b 2 d 1 0",
                          "b 1 a 2 d 1 0",
                          "b 1 a 2 0"]))


def test_gen_possible_subtrees():

    deletion = Deletion(MPTdeletion)
    subtrees = deletion.possible_subtrees(
        MPTdeletion.root.pos, [[bytearray([1])], [bytearray([1])]])
    res = []
    for subtree in subtrees:
        res.append(" ".join((compress(str(MPTdeletion.root.pos).split(" "), subtree))))

    assert_equals(sorted(res), sorted(['2', '1', 'c 2 1']))

"""
def test_substitution():
    subst = sub.Substitution(MPT)
    param = subst.get_parameterization([0,0,0], "a")
    print(param)
    assert_equals(param, ["a", "a", "a"])

    param = subst.get_parameterization([0,1,1], "a")
    print(param)
    assert_equals(param, ["a", "a1", "a1"])

    param = subst.get_parameterization([0,1,2], "a")
    print(param)
    assert_equals(param, ["a", "a1", "a2"])

    param = subst.get_parameterization([2,1,2], "a")
    print(param)
    assert_equals(param, ["a2", "a1", "a2"])
"""

def test_apply_rgs():
    mpt = "a a 0 1 b 2 3"
    param = "a"
    rgs = [1, 0]

    res = sub.apply_rgs(param, rgs, mpt.split(" "))
    assert_equals(res, ["a1", "a", "0", "1", "b", "2", "3"])

    p2 = "b"
    rgs2 = [12]
    subst = sub.Substitution({param: rgs, p2: rgs2})
    mpt = MPT(mpt)
    assert_equals(subst.apply(mpt), "a1 a 0 1 b12 2 3")
