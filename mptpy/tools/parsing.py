""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
import os
import numpy as np
from node import Node
import tools.joint_tree as joint_tree

# TODO remove data
def parse_file(file_path, data=None, form=None):
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

    # TODO check for multiple lines, remove data
    lines = process_file(lines, data=data)
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

    subtrees = []

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


def process_file(model_lines, data=None):
    """ Processes the source file lines by splitting into additive sublists.

    Parameters
    ----------
    _filename : str
        Lines in model file.

    Returns
    -------
    list(str)


    """

    subtrees = []

    print(os.path.abspath("temp/model.restr"))

    # split the model lines at empty lines ([])
    indices = [i for i, x in enumerate(model_lines) if x == '']
    for i, j in zip([0] + indices, indices + [None]):
        i += (i != 0)
        subtrees.append(model_lines[i:j])

    max_params = 0
    for subtree in subtrees:
        max_params += len(subtree) - 1

    if os.path.exists("temp/model.restr"):
        os.remove("temp/model.restr")

    if len(subtrees) > 1:
        if data is not None:
            data = np.genfromtxt(data, delimiter=',', dtype='int')
            if -1 in data[0]:
                data = data[1:]

        subtrees, static_params = joint_tree.join_subtrees(subtrees, data)

        with open("temp/model.restr", "w") as file_:
            for param, value in static_params.items():
                print(param, value)
                file_.write("{} = {}\n".format(param, value))

    else:
        subtrees = subtrees[0]

    return subtrees#, max_params # TODO