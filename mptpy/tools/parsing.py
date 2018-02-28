""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
import string
from node import Node


def parse_file(file_path, form=None):
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
    lines = get_lines(file_path)

    # Infer the format of the source file
    if form is None:
        form = "BMPT"
        if any("*" in line for line in lines):
            form = "easy"

    # TODO check for multiple lines

    return lines[0] if form == "BMPT" else parse_branches(lines)


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
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.split("#")[0].strip() for line in lines]
        return lines


def parse_branches(lines, sep=" "):
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

    tree_str = dict_to_BMPT(tree, sep=sep)
    return tree_str


def dict_to_BMPT(tree, sep=" "):
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

    return root + sep + dict_to_BMPT(pos_tree) + sep + dict_to_BMPT(neg_tree)


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

    root = create_from_nested_node(nested)
    return root
