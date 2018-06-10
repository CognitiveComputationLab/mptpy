""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
import string
from node import Node
from . import joint_tree as joint_tree
from . import transformations as trans


def parse_file(file_path, form=None, sep=' '):
    """ Parse a .txt or .model file and return the MPT model in
    the BMPT form

    Parameters
    ----------
    file_path : str
        path to the model file
    form : ["easy", "BMPT"], optional
        format of the file

    Returns
    -------
    str
        MPT in the BMPT format
    """
    lines, leaves = get_lines(file_path)

    # Infer the format of the source file
    if form is None:
        form = "BMPT"
        if any("*" in line for line in lines):
            form = "easy"

    lines = split_subtrees(lines)

    leaf_test = lambda node: all([ch in string.digits for ch in node])
    if leaves:
        leaf_test = lambda node: node in leaves
    
    if len(lines) > 1 and form == "BMPT":

        lines = bmpt_to_easy(lines, ' ', leaf_test)
        form = "easy"

    prefix_tree = joint_tree.get_prefix_tree(lines)

    lines = prefix_tree.join_subtrees(lines)

    if form == "easy":
        lines = easy_to_bmpt(lines)
    else:
        lines = lines[0]


    return lines, prefix_tree, leaf_test


def get_lines(file_path):
    """ Extracts the formula lines from the source model file.

    Parameters
    ----------
    filepath : str
        Path to the source model file.

    Returns
    -------
    list(str)
        Formula lines of the source model.

    """
    leaves = []
    
    with open(file_path, 'r') as file:
        
        lines = file.readlines()

        leaves = list(filter(lambda x: x[0] == "[", lines))
        if leaves:
            # TODO
            leaves = leaves[0].strip().replace("[", "").replace("]", "").split(", ")

        lines = list(filter(lambda x: x[0] != "[", lines))

        lines = filter(lambda x: x[0] != "#", lines) # get rid of commentary liens
        lines = [line.split("#")[0].strip() for line in lines] # and in-line comments
        
        return lines, leaves


def bmpt_to_easy(lines, sep, leaf_test):
    """ Turns the lines of a tree in the bmpt file format
    to a tree in the easy format

    Parameters
    ----------
    lines : list
        list of lines of the file in the bmpt format
    sep : str
        separator
    leaf_test : func
        function to test for leaves

    Returns
    -------
    str
        Tree in easy form

    """
    lines = [[trans.to_easy(line[0], sep, leaf_test)] for line in lines]
    lines = [subtree[0].rstrip().split("\n") for subtree in lines]
    return lines


def easy_to_bmpt(lines, sep=' '):
    """ Turns the lines of a tree in the easy file format
    to a tree in the formal language

    Parameters
    ----------
    lines : list
        list of lines of the file in the easy format
    sep : str
        separator

    Returns
    -------
    str
        Tree in Formal language form, with sep as separator

    """

    tree = dict()
    for i, line in enumerate(lines):
        line = line.replace(" ", "").strip()
        tree[i] = line.split("+")

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

    root = get_only_parameter(list(tree.values())[0][0][0])

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


def get_only_parameter(probability_str):
    """ Extract the parameter from the string formula.

    Parameters
    ----------
    probability_str : str
        String formula to extract the parameter from.

    Returns
    -------
    str
        Parameter identifier.

    """
    return re.search(r"[A-z_]+\d*", probability_str).group()


def create_from_nested(nested, is_leaf):
    """ Creates tree repersentation from nested and returns its root.

    """

    def create_from_nested_node(nested):
        """ Creates a node object from a nested node.

        """

        if isinstance(nested, list):
            node = nested[0]
        else:
            node = nested
        if is_leaf(node):
            return Node(node, leaf=True)

        node_obj = Node(node, leaf=False)

        neg = nested[1][1]  # right subtree
        pos = nested[1][0]  # left subtree

        node_obj.pos = create_from_nested_node(pos)
        node_obj.neg = create_from_nested_node(neg)

        return node_obj

    if isinstance(nested, list) and len(nested) == 1: # list of only one param
        nested = nested[0]

    root = create_from_nested_node(nested)
    return root


def split_subtrees(model_lines):
    """ If the model contains multiple subtrees, split
    formulae at the empty lines

    Parameters
    ----------
    model_lines : list
        List of lines in the model file
    
    Returns
    -------
    list
        List of subtrees
    """
    subtrees = []
    # split the model lines at empty lines ([])
    indices = [i for i, x in enumerate(model_lines) if x == '']
    for i, j in zip([0] + indices, indices + [None]):
        i += (i != 0)
        subtrees.append(model_lines[i:j])
    return subtrees
