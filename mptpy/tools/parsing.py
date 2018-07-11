""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
from itertools import groupby
import mptpy.tools.transformations as trans

from mptpy.mpt import MPT
from . import joint_tree


class Parser():

    def parse(self, file_path):
        """ Parse the mpt from the file

        Parameters
        ----------
        file_path : str
            path to the model file

        Returns
        -------
        """
        lines = self.open(file_path)
        parser = self.instantiate(lines)
        built = parser.build(lines)
        return built
    
    def build(self, lines):
        subtrees = [
            list(g) for k,
            g in groupby(
                lines,
                key=lambda x: x != '') if k]
        joint = self.build_mpt(subtrees)

        return joint

    def instantiate(self, lines):
        if any(["*" in line or "+" in line for line in lines]):
            parser = EasyParser()
        else:
            parser = BmptParser()
        return parser
    
    def open(self, file_path):
        """ Opens the file and return its contents

        Parameters
        ----------
        file_path : str
            path to the mpt file
        """
        mpt_file = open(file_path, 'r')
        lines = self.strip(mpt_file.readlines())  # remove comments
        mpt_file.close()
        return lines

    def strip(self, lines):
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
        criteria = lambda line: line[0] != "#"
        lines = filter(criteria, lines)  # commentary and empty lines
        lines = [line.split("#")[0].strip() for line in lines]  # in-line

        return lines


class EasyParser(Parser):

    def build_mpt(self, subtrees):
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
        joint.subtrees = subtrees #TODO to easy?
        
        return joint


class BmptParser(Parser):

    def __init__(self):
        self.leaf_test = None

    def build(self, lines):
        leaves = self.get_leaf_info(lines)  # retrieve leaf information
        words = self.get_words(lines)  # retrieve the mpt word
        self.leaf_test = self.construct_leaf_test(leaves)
        return super().build(words)

    def build_mpt(self, subtrees):
        """ Build MPTs from the given subtrees

        Parameters
        ----------
        subtrees : [str]
            List of subtrees

        Returns
        -------

        """
        mpts = []
        for subtree in subtrees:

            bmpt = subtree[0]
            mpts.append(MPT(bmpt, leaf_test=self.leaf_test))

        joint = joint_tree.join(mpts)
        joint.subtrees = subtrees #TODO to easy?
        
        return joint

    def get_leaf_info(self, lines):
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

    def construct_leaf_test(self, leaves):
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
            func = lambda node: node in leaves
        else:
            func = lambda node: all(
                [ch in string.digits for ch in node])
        return func

    def get_words(self, lines):
        """ Retrieve the mpt from the file content

        Parameters
        ----------
        lines : [str]
            file content without comments

        Returns
        -------
        str
            mpt word
        """
        lines = list(filter(lambda x: not x.startswith("["), lines))
        return lines
