""" Transformation operations working on MPTs or BMPT words.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from itertools import filterfalse
from tools.parsing import create_from_nested


def word_to_tree(word):
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
    nested = nested_list(word)
    print("nested ", nested)
    root = create_from_nested(nested, word.is_leaf)
    return root


def tree_to_word(node, sep=" "):
    """ Translate a multinomial processing tree (MPT) to the corresponding word
    in the formal language.

    Parameters
    ----------
    node : Node
        root node of the MPT

    Returns
    -------
    MPTWord
        MPT in the BMPT language format

    """

    if node.leaf:
        return str(node.content)

    pos = tree_to_word(node.pos)
    neg = tree_to_word(node.neg)
    return node.content + sep + pos + sep + neg


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
    lines = get_lines(nested_list(mpt.word), dict())

    easy = ""
    for key in sorted(lines.keys()):
        line = " + ".join(lines[key]) + "\n"
        easy += line
    return easy


def get_lines(subtree, lines, temp=""):
    """ Builds a dictionary of the answers and the
    respective branch formulas

    Parameters
    ----------
    subtree : list
        tree as a nested list

    lines : dict
        empty dictionary to be filled

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

        get_lines(pos, lines, temp + subtree[0] + left_mult)
        get_lines(neg, lines, temp + "(1-" + subtree[0] + ")" + right_mult)

        return lines

    else:
    # we reached the leaf
        key = int(subtree)
        if key not in lines:
            lines[key] = []
        lines[key] += [temp]

# TODO
def nested_list(word):
    """Turns a word for a subtree into a nested list
    Parameters
    ----------
    str_ : str
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
