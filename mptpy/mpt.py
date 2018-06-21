""" Data structure for Multinomial Processing Trees (MPTs).

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""

import os
from mpt_word import MPTWord
import tools.transformations as trans # pylint: disable=import-error
from visualization.visualize_mpt import cmd_draw # pylint: disable=import-error


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

        # mpt given as word
        if isinstance(mpt, str):
            self.word = MPTWord(mpt, sep=sep, leaf_test=leaf_test)
            self.root = trans.word_to_nodes(self.word)
        
        # mpt given as root node
        else:
            self.root = mpt
            self.word = MPTWord(str(self))

    def max_parameters(self):
        """ The maximal number of free parameters in the model

        Returns
        -------
        int
            max number of free parameters
        """
        return sum([len(subtree) - 1 for subtree in self.subtrees])

    def get_formulae(self):
        """ Extracts the branch formulae underlying the represented MPT.

        Returns
        -------
        formulae : list(str)
            List of strings representing the branch formulae of the represented
            MPT.

        classes : list(str)
            Outcome category identifiers corresponding the the branch formulae.
        """
        if len(list(self.word)) == 1:
            return [''], [str(self)]

        # Obtain this trees information
        param = self.word[0]
        subtrees = self.word.split_pos_neg()

        # Obtain the subtree branch formulae
        pos_sub_branches = MPT(
            subtrees[0],
            self.word.sep,
            self.word.is_leaf).get_formulae()
        neg_sub_branches = MPT(
            subtrees[1],
            self.word.sep,
            self.word.is_leaf).get_formulae()

        # Update the subtree formulae with current parameter
        pos_branches = [
            "{} * {}".format(param, x) for x in pos_sub_branches[0]
        ]
        neg_branches = [
            "(1 - {}) * {}".format(param, x) for x in neg_sub_branches[0]
        ]
        comb_branches = pos_branches + neg_branches

        # Combine the subtrees to construct formulae and classes.
        # Simultaneously remove the trailing multiplication operators which are
        # added in the computation of positive and negative branches above.
        formulae = [x[:-3] if x.endswith(' * ') else x for x in comb_branches]
        classes = pos_sub_branches[1] + neg_sub_branches[1]

        return formulae, classes

    def save(self, path, form="easy"):
        """ Saves the tree to a file

        Parameters
        ----------
        path : str
            where to save the tree
        """

        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_ = open(path, "w")

        to_print = trans.to_easy(self) if form == "easy" else self.word.str_
        file_.write(to_print)
        file_.close()

    def draw(self):
        """ Draw MPT to the command line """
        cmd_draw(self.word)

    def __eq__(self, other):
        print("hello")
        print(str(self))
        print(str(other))
        return self.word.abstract() == other.word.abstract()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        sep = " "
        def fos(node):
            if node.leaf:
                return str(node.content)

            pos = fos(node.pos)
            neg = fos(node.neg)
            return node.content + sep + pos + sep + neg
        return fos(self.root)
