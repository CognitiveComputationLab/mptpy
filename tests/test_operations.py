""" Tests the operations on MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from nose.tools import assert_equals, assert_false
from itertools import compress
from tests.context import mptpy
from mptpy.tools import transformations, parsing
from mptpy.node import Node
from mptpy.mpt_word import MPTWord
from mptpy.mpt import MPT
from mptpy.optimization.operations.deletion import Deletion


def test_deletion():
    s = "b c 2 1 a 2 d 1 0"

    '''
            b
      c           a
    2   1       2   d
                   1  0
    '''

    mpt = MPT(s)

    deletion = Deletion(mpt)
    candidates = deletion.generate_candidates()
    print()

    print("candidates:", candidates)
    print()

    assert_equals(sorted(candidates), sorted([s, "b c 2 1 a 2 0", "b c 2 1 d 1 0", "b c 2 1 0", 
    "b 2 a 2 d 1 0", "b 2 d 1 0", "b 1 a 2 d 1 0", "b 1 a 2 0", "a 2 d 1 0"]))

def test_get_levels():
    s = "b c 2 1 a 2 d 1 0"

    mpt = MPT(s)

    deletion = Deletion(mpt)

    levels = deletion.get_levels()
    levels = {key: [node.content for node in value] for key, value in levels.items()}
    print(levels)
    assert_equals({0:["b"], 1:["c","a"], 2:["2", "1", "2", "d"], 3:["1","0"]}, levels)


def test_gen_possible_subtrees():
    s = "b c 2 1 a 2 d 1 0"

    mpt = MPT(s)

    deletion = Deletion(mpt)
    subtrees = deletion.generate_possible_subtrees(mpt.root.pos, [[[1]], [[1]]])
    res = []
    for subtree in subtrees:
        res.append(" ".join((compress(str(mpt.root.pos).split(" "), subtree))))

    assert_equals(sorted(res), sorted(['2', '1', 'c 2 1']))