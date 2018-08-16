""" Transformation operations working on MPTs or BMPT words.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
from collections import OrderedDict
from mptpy.node import Node


def word_to_nodes(word, idx=0):
    """ Translate an MPT in the BMPT language (see Purdy & Batchelder 2009) to
    a binary tree

    Parameters
    ----------
    word : MPTWord
        MPT in the BMPT language format

    Returns
    -------
    Node
        root node of the MPT

    """
    node = Node(word[idx])

    if not word.is_leaf(word[idx]):
        node.pos = word_to_nodes(word, idx=idx + 1)
        node.neg = word_to_nodes(word, idx=idx + 1 + len(node.pos))

    return node


def to_easy(mpt):
    """ Transforms the MPT to the easy format

    Parameters
    ----------
    mpt : MPT
        MPT model

    Returns
    -------
    str
        tree in the easy format

    """

    lines = get_formulae(mpt)

    easy = ""
    for key in sorted(lines.keys()):
        line = " + ".join(lines[key]) + "\n"
        easy += line
    return easy


def easy_to_bmpt(lines, sep=' ', leaf_step=0):
    """ Turns the lines of a tree in the easy file format
    to a tree in the formal language

    Parameters
    ----------
    lines : list
        list of lines of the file in the easy format
    sep : str
        separator
    leaf_step : int

    Returns
    -------
    str
        Tree in Formal language form, with sep as separator

    """

    tree = dict()
    for i, line in enumerate(lines):
        leaf_name = i + leaf_step
        line = line.replace(" ", "").strip()
        tree[leaf_name] = line.split("+")

    for answer in tree.items():
        for i, branch in enumerate(answer[1]):
            answer[1][i] = branch.split("*")

    tree_str = dict_to_bmpt(tree, sep=sep)

    return tree_str


def dict_to_bmpt(tree, sep=" "):
    """ Turns a dictionary of answers and corresponding branches
    to a tree in the formal language

    Parameters
    ----------
    tree : dict
        answers and corresponding branches

    Returns
    -------
    str
        Tree in Formal language form, with " " as separator

    """

    if len(tree.keys()) == 1 and list(tree.items())[0][1] == [[]] :
        return str(list(tree.keys())[0])

    # match the parameters : letter(s) + optional number
    root = re.search(r"[A-z_]+\d*", list(tree.values())[0][0][0]).group()

    pos_tree, neg_tree = split_tree(tree)

    res= sep.join([root, dict_to_bmpt(pos_tree), dict_to_bmpt(neg_tree)])

    return res


def split_tree(tree):
    """ Splits the dictionary of answers and corresponding branches
    to the positive and the negative subtrees

    Parameters
    ----------
    tree : dict
        answers and corresponding branches

    Returns
    -------
    tuple
        positive subtree, negative subtree
    """
    neg_tree = dict()
    pos_tree = dict()

    for answer in tree.items():
        for branch in answer[1]:
            subtree = pos_tree if '1-' not in branch[0] else neg_tree

            if answer[0] not in subtree.keys():
                subtree[answer[0]] = []
            subtree[answer[0]].append(branch[1:])

    return pos_tree, neg_tree


def get_formulae(mpt):
    """ Builds a dictionary of the answers and the
    respective branch formulas

    Parameters
    ----------
    mpt : MPT

    Returns
    -------
    dict(int, string)
        Dictionary of the answer categories of the tree and the branch formulas

    """
    lines = {answer : [] for answer in mpt.word.answers}
    def recursive_to_formulae(node, temp=""):
        """ Recursively compute the branch formulae """
        if node.leaf:
            lines[node.content] += [temp]
            return None

        left_mult = "" if node.pos.leaf else " * "
        right_mult = "" if node.neg.leaf else " * "

        recursive_to_formulae(node.pos, temp +
                              node.content + left_mult)
        recursive_to_formulae(node.neg, temp +
                              "(1-" + node.content + ")" + right_mult)

        return lines

    formulae = recursive_to_formulae(mpt.root)
    ordered = OrderedDict()
    for key in sorted(formulae, key=int):
        ordered[key] = formulae[key]

    return ordered
