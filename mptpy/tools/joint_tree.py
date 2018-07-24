""" This scripts implements an algorithm to convert joint models into
equivalent single-tree models.

Copyright 2017 Cognitive Computation Lab
University of Freiburg
Nicolas Riesterer <riestern@tf.uni-freiburg.de>

"""

import math

from mptpy.node import Node
import mptpy.mpt
from mptpy.tools import misc


def join(args, prefix_no=0):
    """ Join two MPTs with dummy nodes

    Arguments
    ---------
    args : list
        list of mpts

    Returns
    -------
    MPT
        joint mpt
    """

    if len(args) <= 1:
        return args[0]

    left, right = misc.split_half(args)

    left_child = join(left, prefix_no + int(math.ceil(len(args) / 2))).root
    right_child = join(right, prefix_no + 1).root

    dummy = Node("y" + str(prefix_no), left_child, right_child)

    new_is_leaf = lambda x: any([mpt.word.is_leaf(x) for mpt in args])
    return mptpy.mpt.MPT(dummy, leaf_test=new_is_leaf)
