""" Data structure for Multinomial Processing Trees (MPTs).

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""

from mpt_word import MPTWord
from node import Node
from tools.transformations import word_to_tree, tree_to_word
from tools.parsing import parse_file


def build_from_file(file_path, form=None):
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
    word = parse_file(file_path, form=form)
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
            self.root = mpt
            self.word = tree_to_word(self.root, sep=sep)

        # mpt given as word
        elif isinstance(mpt, str):
            self.word = MPTWord(mpt, sep=sep)
            if is_leaf:
                self.word.set_is_leaf(is_leaf)
            self.root = word_to_tree(self.word, sep=sep)


    def get_formulae(self):
        """ Extracts the branch formulae underlying the represented MPT.

        Returns
        -------
        formulae : list(str)
            List of strings representing the branch formulae of the represented
            MPT.

        classes : list(str)
            Outcome category identifiers corresponding the the branch formulae.

        Examples
        --------
        >>> MPT('pAB').branch_formulae()
        (['p', '(1 - p)'], ['A', 'B'])
        >>> MPT('rNgNO').branch_formulae()
        (['r', '(1 - r) * g', '(1 - r) * (1 - g)'], ['N', 'N', 'O'])

        """
        raise NotImplementedError

    def to_easy(self):
        """ Tree in easy format """

        raise NotImplementedError

    def to_string(self):
        """ Tree in formal language format """

        raise NotImplementedError

    def save(self, path):
        """ Saves the tree to a file

        Parameters
        ----------
        path : str
            where to save the tree
        """

        raise NotImplementedError

    def __eq__(self, other):
        return self.word.abstract() == other.word.abstract()

    def __ne__(self, other):
        return not self.__eq__(other)
