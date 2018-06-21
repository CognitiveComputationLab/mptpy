""" This scripts implements an algorithm to convert joint models into
equivalent single-tree models.

Copyright 2017 Cognitive Computation Lab
University of Freiburg
Nicolas Riesterer <riestern@tf.uni-freiburg.de>

"""

import numpy as np
from mptpy.node import Node
import mptpy.mpt


def split_half(args):
    """ Split the given list into two parts (equal if possible, if not 
    the right one gets one more)

    Arguments
    ---------
    args : list
        list to split

    Returns
    -------
    list, list
        Args split in two parts
    """
    split = len(args) / 2

    left = args[:int(np.floor(split))]
    right = args[int(np.floor(split)):]

    return left, right


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

    left, right = split_half(args)

    left_child = join(left, prefix_no + int(np.ceil(len(args) / 2))).root
    right_child = join(right, prefix_no + 1).root

    return mptpy.mpt.MPT(Node("y" + str(prefix_no), left_child, right_child))


def comp_param_ratios(observations, prefix_no=0):
    if len(observations) <= 1:
        return {}

    left, right = split_half(observations)

    param_ratio = np.sum(left) / np.sum(observations)

    result_dict = {"{}{}".format("y", prefix_no): param_ratio}

    left_prefix = prefix_no + int(np.ceil(len(observations) / 2))
    result_dict.update(comp_param_ratios(left, left_prefix))

    result_dict.update(comp_param_ratios(right, prefix_no + 1))

    return result_dict


def compute_ratios(data, subtrees):
    subtree_observations = []
    idx = 0
    for subtree in subtrees:
        n_cats = len(subtree)
        subtree_observations.append(data[idx:(idx + n_cats)].sum())
        idx += n_cats
    subtree_observations = np.array(subtree_observations)

    ratios = comp_param_ratios(subtree_observations)
    return ratios
