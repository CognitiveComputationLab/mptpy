""" Data structure for Multinomial Processing Trees (MPTs).

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""

from mptpy.mpt_word import MPTWord
import mptpy.tools.transformations as trans  # pylint: disable=import-error
from mptpy.visualization.visualize_mpt import cmd_draw  # pylint: disable=import-error
from mptpy.tools import misc


class MPT(object):
    """ Multinomial Processing Tree (MPT) data structure.

    """

    def __init__(self, mpt, sep=" ", leaf_test=None):
        """ Constructs the MPT object.

        Parameters
        ----------
        mpt : [str, Node]
            either tree in bmpt or as root object.

        """
        self.subtrees = []
        self.word = None
        self.root = None

        # mpt given as word
        if isinstance(mpt, str):
            self.word = MPTWord(mpt, sep=sep, leaf_test=leaf_test)
            self.root = trans.word_to_nodes(self.word)

        # mpt given as root node
        else:
            self.root = mpt
            self.word = MPTWord(str(self))

    @property
    def params(self):
        return self.word.parameters

    @property
    def categories(self):
        return self.word.answers

    def formulae(self):
        """ Calculate the branch formulae for the categories in the tree

        Returns
        -------
        dict
            {category : formulae}
        """
        return trans.get_formulae(self)

    def max_parameters(self):
        """ The maximal number of free parameters in the model

        Returns
        -------
        int
            max number of free parameters
        """
        return sum([len(subtree) - 1 for subtree in self.subtrees])

    def get_levels(self, node, level=0):
        """ Generate a dict with all nodes and their respective level
        0 is the root

        Parameters
        ----------
        node : Node
            starting node

        level : int, optional
            level from which to start counting
        """
        levels = {level: [node]}

        if not node.leaf:
            left_dict = self.get_levels(node.pos, level=level + 1)
            right_dict = self.get_levels(node.neg, level=level + 1)

            temp = misc.merge_dicts(left_dict, right_dict)
            levels.update(temp)

        return levels

    def save(self, path, form="easy"):
        """ Saves the tree to a file

        Parameters
        ----------
        path : str
            where to save the tree
        """
        to_print = trans.to_easy(self) if form == "easy" else self.word.str_
        misc.write_iterable_to_file(path, to_print, newline=False)

    def draw(self):
        """ Draw MPT to the command line """
        cmd_draw(self)

    def __eq__(self, other):
        return self.word.abstract() == other.word.abstract()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.word:
            return self.word.str_

        sep = " "

        def dfs(node):
            """ depth first search """
            if node.leaf:
                return str(node.content)

            pos = dfs(node.pos)
            neg = dfs(node.neg)
            return node.content + sep + pos + sep + neg

        return dfs(self.root)
