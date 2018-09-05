""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
import re

import numpy as np
from itertools import groupby
import mptpy.tools.transformations as trans

from mptpy.mpt import MPT
from . import joint_tree


def construct_leaf_test(leaves):
    """ Constructs the test for leaves

    Parameters
    ----------
    leaves : [str]
        list of leaf names

    Returns
    -------
    func
        leaf test
    """
    if leaves:
        return lambda node: node in leaves

    return lambda node: all([ch in string.digits for ch in node])


def get_leaf_info(lines):
    """ If there is information about the leaves in the file,
    retrieve and return it

    Parameters
    ----------
    lines : [str]
        file content without comments

    Returns
    -------
    [str]
        list with leaf names
    """
    leaves = list(filter(lambda x: x.startswith("["), lines))
    if leaves:
        leaves = leaves[0].strip()
        leaves = leaves.replace("[", "").replace("]", "").split(",")
        leaves = [leaf.lstrip() for leaf in leaves]
    return leaves


def strip(lines):
    """ Removes comments, new lines and empty lines from the file content

    Parameters
    ----------
    lines : [str]
        file content

    Returns
    -------
    [str]
        file content without comments
    """
    lines = filter(lambda line: line[0] != "#", lines)  # commentary and empty lines
    lines = [line.split("#")[0].strip() for line in lines]  # in-line

    return lines


def open_model(file_path):
    """ Opens the file and return its contents

    Parameters
    ----------
    file_path : str
        path to the mpt file
    """
    with open(file_path, 'r') as mpt_file:
        lines = strip(mpt_file.readlines())  # remove comments

    return [escape_parameters(x) for x in lines]

def escape_parameters(formula, escape_char='_'):
    """ Escapes the parameters of a category formula.

    Parameters
    ----------
    formula : str
        Category formula.

    escape_char : str, optional
        Character string to escape parameters with (prepended and appended to
        variables).

    Note
    ----
    Currently, the algorithm fails to correctly account for variables starting
    with a '1'.

    Examples
    --------
    >>> escape_parameters('a * b * c')
    '_a_ * _b_ * _c_'
    >>> escape_parameters('e * ee * a * ea * _ba')
    '_e_ * _ee_ * _a_ * _ea_ * __ba_'
    >>> escape_parameters('a1 * a2 * e1a')
    '_a1_ * _a2_ * _e1a_'

    """

    escaped = ''

    reading_mode = False
    for char in formula:
        if char not in ['*', '(', ')', '+', ' ', '-', '1']:
            if not reading_mode:
                escaped += escape_char
                reading_mode = True

        if char in ['*', '(', ')', '+', ' ', '-']:
            if reading_mode:
                escaped += escape_char
                reading_mode = False

        escaped += char

    if reading_mode:
        escaped += escape_char

    return escaped

class Parser():
    """ Parsing for easy format """

    def parse(self, file_path):
        """ Parse the mpt from the file

        Parameters
        ----------
        file_path : str
            path to the model file

        Returns
        -------
        """
        lines = open_model(file_path)
        parser = self.instantiate(lines)
        built = parser.build(lines)
        return built

    def build(self, lines):
        """ Build MPT from lines. Can have multiple subtrees.
        """
        subtrees = [
            list(g) for k,
            g in groupby(
                lines,
                key=lambda x: x != '') if k]
        joint = self.build_mpt_from_subtrees(subtrees)

        return joint

    def build_mpt_from_subtrees(self, subtrees):
        """ Build MPTs from the given subtrees

        Parameters
        ----------
        subtrees : [str]
            List of subtrees

        Returns
        -------

        """
        mpts = []
        leaf_step = 0

        for subtree in subtrees:
            # transform each subtree to bmpt
            bmpt = trans.easy_to_bmpt(subtree, leaf_step=leaf_step)
            mpts.append(MPT(bmpt))
            leaf_step += len(subtree)

        joint = joint_tree.join(mpts)
        joint.subtrees = subtrees  # TODO to easy?

        return joint

    def instantiate(self, lines):
        """ Checks if we have a '*' or '+' in the file.
        If yes, assumes the file is in easy. else bmpt

        Parameters
        ----------
        lines : [str]
            lines in the file
        """
        if any(["*" in line or "+" in line for line in lines]):
            return self

        return BmptParser()


class BmptParser(Parser):
    """ Parsing for BMPT format """

    def __init__(self):
        self.leaf_test = None

    def build(self, lines):
        """ Build MPT from lines. Can have multiple subtrees.
        """
        leaves = get_leaf_info(lines)  # retrieve leaf information
        words = list(
            filter(
                lambda x: not x.startswith("["),
                lines))  # retrieve the mpt word
        self.leaf_test = construct_leaf_test(leaves)
        return super().build(words)

    def build_mpt_from_subtrees(self, subtrees):
        """ Build MPTs from the given subtrees

        Parameters
        ----------
        subtrees : [str]
            List of subtrees

        Returns
        -------
        joint tree
        """
        mpts = []
        for subtree in subtrees:

            bmpt = subtree[0]
            mpts.append(MPT(bmpt, leaf_test=self.leaf_test))

        joint = joint_tree.join(mpts)
        joint.subtrees = subtrees  # TODO to easy?

        return joint
