""" Module for visualizations of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


def to_tikz(mpt):
    """ Generate tikz code for given MPT
    Parameters
    ----------
    mpt : MPT
        MPT to be translated to tikz

    code_path : str
        specify where to save the tikz code
    """

    def recursive_translation(node):
        """ Recursively turn list to str """
        if node.leaf:
            return node.content
        pos = recursive_translation(node.pos)
        neg = recursive_translation(node.neg)
        return "[.{} {} {} ]".format(node.content, pos, neg)

    return r"\Tree " + recursive_translation(mpt.root)


def cmd_draw(mpt):
    """ Draw the mpt to the command line

    Parameters
    ----------
    mpt : MPT
        MPT to be drawn
    """
    #word = mpt

    #subtree = transformations.nested_list(word)
    _dfs_print(mpt.root)


def _dfs_print(node, depth=0):
    """ Prints a tree recursively via depth first search

    Parameters
    ----------
    subtree : list
        tree as a nested list

    """
    to_print = '\t' * depth

    if node.leaf:  # leaf
        to_print += node.content
        print(to_print)
        return

    _dfs_print(node.pos, depth + 1)
    to_print += node.content  # current node
    print(to_print)
    _dfs_print(node.neg, depth + 1)
