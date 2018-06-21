""" Transformation operations working on MPTs or BMPT words.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
from itertools import filterfalse
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



def to_easy(mpt, sep=' ', leaf_test=None):
    """ Transforms the MPT to the easy format

    Parameters
    ----------
    mpt : [MPT, MPTWord, str]
        MPT model as either MPT or MPTWord object or str

    Returns
    -------
    str
        tree in the easy format

    """
    if type(mpt).__name__ == "MPT":
        mpt = mpt.word

    elif isinstance(mpt, str):
        nested = _parse_tree(mpt.split(sep), leaf_test)[0]
        answers = filter(leaf_test, mpt.split(sep))
        answer_set = list(OrderedDict.fromkeys(answers))
        lines = _get_lines(nested, dict(), answer_set)

    if type(mpt).__name__ == "MPTWord":
        answer_set = list(OrderedDict.fromkeys(mpt.answers))
        lines = _get_lines(nested_list(mpt), dict(), answer_set)

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

    if len(tree.keys()) == 1:
        return str(list(tree.keys())[0])

    # match the parameters : letter(s) + optional number
    root = re.search(r"[A-z_]+\d*", list(tree.values())[0][0][0]).group()

    pos_tree, neg_tree = split_tree(tree)

    return root + sep + dict_to_bmpt(pos_tree) + sep + dict_to_bmpt(neg_tree)


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


def _get_lines(subtree, lines, answer_set, temp=""):
    """ Builds a dictionary of the answers and the
    respective branch formulas

    Parameters
    ----------
    subtree : list
        tree as a nested list

    lines : dict
        empty dictionary to be filled

    answer_set : list
        list of all answers without replications

    Returns
    -------
    dict(int, string)
        Dictionary of the answer categories of the tree and the branch formulas

    """

    if isinstance(subtree, list):
        neg = subtree[1][1]  # right subtree
        pos = subtree[1][0]  # left subtree

        left_mult = " * " if isinstance(pos, list) else ""
        right_mult = " * " if isinstance(neg, list) else ""

        _get_lines(pos, lines, answer_set, temp + subtree[0] + left_mult)
        _get_lines(neg, lines, answer_set, temp +
                   "(1-" + subtree[0] + ")" + right_mult)

        return lines

    else:
        # we reached the leaf

        key = answer_set.index(subtree)
        if key not in lines:
            lines[key] = []
        lines[key] += [temp]


def nested_list(word):
    """Turns a word for a subtree into a nested list
    Parameters
    ----------
    word : MPTWord
        tree in string form

    Returns
    -------
    list
        nested list of nodes and leaves in subtree
    """

    str_ = word.str_.split(word.sep)

    # if only leaf
    if len(str_) == 1:
        return str_

    subtrees = _parse_tree(str_, word.is_leaf)
    return subtrees[0]


def _pop_down(stack):
    """Appends the last element on the stack to the one below

    Parameters
    ----------
    stack : list

    Returns
    -------
    list
        stack with the "full" elements on top merged down
    """
    temp = stack.pop()
    if len(stack[-1]) == 2:
        stack[-1][1].append(temp)
    else:
        stack[-1].append([temp])


def _parse_tree(str_, is_leaf):
    """ Parse the mpt word and translate it to a nested list
    Parameters
    ----------
    str_ : str
        tree in str form

    Returns
    -------
    list
        mpt as a nested list
    """
    num_params = len(list(filterfalse(is_leaf, str_)))
    num_children = []

    # initialize num_children to -1 for all inner nodes
    for _ in range(num_params):
        num_children.append(-1)

    stack = []

    for char in str_:

        if not is_leaf(char):
            # if char is a parameter, add it to the stack
            stack.append([char])

        else:
            # else if answer, add it to the last parameter in the stack
            if len(stack[-1]) > 1:
                stack[-1][1].append(char)
            else:
                stack[-1].append([char])

        if len(stack[-1]) > 1:
            # if last thing on stack is "full", append downwards
            while len(stack[-1][1]) == 2 and len(stack) > 1:
                _pop_down(stack)

    # cleanup
    while len(stack) > 1:
        _pop_down(stack)

    return stack
