""" Module for visualizations of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""
import json
import tools.transformations as transformations


def to_tikz(mpt):
    """ Generate tikz code for given MPT
    Parameters
    ----------
    mpt : MPT
        MPT to be translated to tikz

    code_path : str
        specify where to save the tikz code
    """

    def recursive_translation(subtree, temp=""):
        if not isinstance(subtree, list):
            return subtree
        pos = recursive_translation(subtree[1][0])
        neg = recursive_translation(subtree[1][1])
        return "[." + subtree[0] + " " + pos + " " + neg + " ]"

    nested = transformations.nested_list(mpt.word)
    return r"\Tree " + recursive_translation(nested)



def cmd_draw(mpt):
    """ Draw the mpt to the command line

    Parameters
    ----------
    mpt : MPTWord
        MPT to be drawn
    """
    word = mpt

    subtree = transformations.nested_list(word)
    _dfs_print(subtree, word.is_leaf)


def _dfs_print(subtree, is_leaf, depth=0):
    """ Prints a tree recursively via depth first search

    Parameters
    ----------
    subtree : list
        tree as a nested list

    """
    to_print = '\t' * depth

    if not isinstance(subtree, list): # leaf
        to_print += subtree
        print(to_print)
        return

    neg = subtree[1][1]  # negative subtree
    pos = subtree[1][0]  # positive subtree

    _dfs_print(neg, is_leaf, depth + 1)
    to_print += subtree[0] # current node
    print(to_print)
    _dfs_print(pos, is_leaf, depth + 1)
