""" Data structure for Multinomial Processing Trees (MPTs).

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""

import os
from mpt_word import MPTWord
from node import Node
from tools.transformations import word_to_tree, tree_to_word, to_easy
from tools.parsing import parse_file
from visualization.visualize_mpt import cmd_draw

# TODO remove data
def build_from_file(file_path, data=None, form=None):
    """ Build MPT object from a file (.model or .txt)

    Parameters
    ----------
    file_path : str
        path to the MPT model (.model or .txt)

    Returns
    -------
    MPT
        MPT object constructed from the file
    """
    word = parse_file(file_path, data=data, form=form)

    return MPT(word)


class MPT(object):
    """ Multinomial Processing Tree (MPT) data structure.

    """

    def __init__(self, mpt, sep=" ", is_leaf=None):
        """ Constructs the MPT object.

        Parameters
        ----------
        obj : str
            String object.

        """

        # mpt given as root node
        if isinstance(mpt, Node):
            print(mpt)
            self.root = mpt
            self.word = tree_to_word(self.root, sep=sep)

        # mpt given as word
        elif isinstance(mpt, str):
            self.word = MPTWord(mpt, sep=sep)
            if is_leaf:
                self.word.is_leaf = is_leaf
            self.root = word_to_tree(self.word)

    def to_string(self):
        """ Convenience function to retrieve the string representation

        Returns
        -------
        str
            string representation
        """
        return self.word.str_


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
        word = self.to_string()
        if len(word) == 1:
            return [''], [word]

        # Obtain this trees information
        param = word[0]
        subtrees = self.word.split()
        print(subtrees)

        # Obtain the subtree branch formulae
        pos_sub_branches = MPT(subtrees[0], self.word.sep, self.word.is_leaf).get_formulae()
        neg_sub_branches = MPT(subtrees[1], self.word.sep, self.word.is_leaf).get_formulae()

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

    def to_easy(self):
        """ Transforms the MPT to the easy format

        Returns
        -------
        str
            tree in the easy format

        """
        return to_easy(self)

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

        to_print = to_easy(self) if form == "easy" else self.word.str_
        file_.write(to_print)
        file_.close()

    def draw(self):
        """ Draw MPT to the command line """
        cmd_draw(self.word)

    def __eq__(self, other):
        return self.word.abstract() == other.word.abstract()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "MPT: " + self.word.str_
