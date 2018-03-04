""" This scripts implements an algorithm to convert joint models into
equivalent single-tree models.

Copyright 2017 Cognitive Computation Lab
University of Freiburg
Nicolas Riesterer <riestern@tf.uni-freiburg.de>

"""

import sys
import os
import datetime

import numpy as np

from coco.mpt import parser as cp

class PrefixNode(object):
    def __init__(self, left=None, right=None, content='.'):
        self.left = left
        self.right = right
        self.content = content

    def to_string(self):
        left = self.left.to_string() if self.left is not None else '.'
        right = self.right.to_string() if self.right is not None else '.'
        return '({}) - ({})'.format(left, right)

    def to_formulae(self):
        left_formulae = self.left.to_formulae() if self.left else None
        right_formulae = self.right.to_formulae() if self.right else None

        # Combine the formulae
        left = [str(self.content)]
        if left_formulae:
            left = ['{} * {}'.format(self.content, f) for f in left_formulae]

        right = ['(1 - {})'.format(self.content)]
        if right_formulae:
            right = ['(1 - {}) * {}'.format(self.content, f) for f in right_formulae]

        return left + right

    def set_parameters(self, param_list):
        if not param_list:
            return

        self.content = param_list[0]

        remaining_params = param_list[1:]
        left_slice = int(np.ceil(len(remaining_params) / 2))
        if self.left:
            self.left.set_parameters(remaining_params[left_slice:])
        if self.right:
            self.right.set_parameters(remaining_params[:left_slice])

    def static_parameters(self):
        params = {self.content : 0}

        left = self.left.static_parameters() if self.left else {}
        right = self.right.static_parameters() if self.right else {}

        # merge the subtrees
        params.update(left)
        params.update(right)

        return params

    def comp_param_ratios(self, observations):
        n_left = len(self.left.to_formulae()) if self.left else 1
        n_right = len(self.right.to_formulae()) if self.right else 1

        param_ratio = np.sum(observations[:n_left]) / np.sum(observations)

        result_dict = {self.content: param_ratio}
        if n_left > 1:
            result_dict.update(self.left.comp_param_ratios(observations[:n_left]))
        if n_right > 1:
            result_dict.update(self.right.comp_param_ratios(observations[n_left:]))
        return result_dict

def generate_prefix_tree(n_subtrees):
    if n_subtrees <= 1:
        return None

    left_child = generate_prefix_tree(np.floor(n_subtrees / 2))
    right_child = generate_prefix_tree(np.ceil(n_subtrees / 2))

    return PrefixNode(left_child, right_child)

def merge_trees(prefix_formulae, subtrees):
    n_subtrees = len(subtrees)
    merged = []
    for subtree_idx in range(n_subtrees):
        prefix = prefix_formulae[subtree_idx]
        cat_formulae = subtrees[subtree_idx]
        merged_subtree = []

        for cat_formula in cat_formulae:
            merged_cat_formulae = []
            branch_formulae = cat_formula.split('+')

            for branch_formula in branch_formulae:
                merged_branch_formula = '{} * {}'.format(prefix.strip(), branch_formula.strip())
                merged_cat_formulae.append(merged_branch_formula)

            merged_subtree.append(' + '.join(merged_cat_formulae))

        merged.append(merged_subtree)

    return merged

def generate_prefix_parameters(n_subtrees):
    n_prefix_params = n_subtrees - 1
    n_leading_zeros = int(np.ceil(np.log10(n_prefix_params)))
    param_numbers = [str(x).zfill(n_leading_zeros) for x in np.arange(n_prefix_params)]
    prefix_params = ['{}{}'.format(x, y) for x, y in zip(['y'] * n_prefix_params, param_numbers)]
    return prefix_params


def compute_rations(n_subtrees, subtrees, data, prefix_tree):
    subtree_observations = []
    idx = 0
    for subtree_idx in range(n_subtrees):
        n_cats = len(subtrees[subtree_idx])
        subtree_observations.append(data[idx:(idx+n_cats)].sum())
        idx += n_cats
    subtree_observations = np.array(subtree_observations)

    ratios = prefix_tree.comp_param_ratios(subtree_observations)
    return ratios

def join_subtrees(subtrees, data=None):
    n_subtrees = len(subtrees)

    # Generate the prefix tree
    prefix_tree = generate_prefix_tree(n_subtrees)

    # Assign the parameters
    prefix_params = generate_prefix_parameters(n_subtrees)
    prefix_tree.set_parameters(prefix_params)
    prefix_formulae = prefix_tree.to_formulae()

    # Merge the trees
    merged_subtrees = merge_trees(prefix_formulae, subtrees)
    merged_tree = [f for sub in merged_subtrees for f in sub]

    # Compute parameter ratios and print as MPT restrictions
    if data is not None:
        ratios = compute_rations(n_subtrees, subtrees, data, prefix_tree)
    else:
        ratios = prefix_tree.static_parameters()

    return merged_tree, ratios