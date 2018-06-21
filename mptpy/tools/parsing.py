""" Functions for parsing MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


from itertools import groupby
import mptpy.tools.transformations as trans

from mptpy.mpt import MPT
from . import joint_tree


class AbstractParser():
    
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


class EasyParser(AbstractParser):

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

        subtrees = [
            list(g) for k,
            g in groupby(
                lines,
                key=lambda x: x != '') if k]
        return self.build_mpt(subtrees)

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
        joint.subtrees = subtrees

        return joint


class BmptParser(AbstractParser):

    def __init__(self):
        self.leaves = []
        self.word = ""
        self.leaf_test = None

    def parse(self, file_path):
        """ Parse the mpt from the file

        Parameters
        ----------
        file_path : str
            path to the model file

        Returns
        -------
        """
        pass

    def open(self, file_path):
        """ Opens the file and stores its contents

        Parameters
        ----------
        file_path : str
            path to the mpt file
        """
        lines = super().open(file_path)
        self.leaves = self.get_leaf_info(lines)  # retrieve leaf information
        self.word = self.get_word(lines)  # retrieve the mpt word
        self.leaf_test = self.construct_leaf_test(self.leaves)

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
        leaves = list(filter(lambda x: x[0] == "[", lines))
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
        def func(ch): return ch in leaves
        return func

    def get_word(self, lines):
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
        lines = list(filter(lambda x: x[0] != "[", lines))
        word = lines[0]
        return word
