""" Class module for MPTs in the BMPT language.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
from itertools import filterfalse

class MPTWord(object):
    """ MPT in the BMPT format """

    def __init__(self, word, sep=" "):
        self.word = word
        self.sep = sep

        # defines what characterizes a leaf node
        self.is_leaf = lambda node: all([ch in string.digits for ch in node])

    def set_is_leaf(self, func):
        """ Set the characteristic function of a leaf node
        Parameters
        ----------
        func : function
            The characteristic function of a leaf node -
            by default: lambda node: all([ch in string.digits for ch in node])

        """
        self.is_leaf = func

    def get_answers(self):
        """ Return all the answers

        Returns
        -------
        list
            list of all the answers, with duplicates
        """
        split = self.word.split(self.sep)
        return list(filter(self.is_leaf, split))

    def get_parameters(self):
        """ Return all the (inner node) parameters

        Returns
        -------
        list
            list of all the parameters, with duplicates
        """
        split = self.word.split(self.sep)
        return list(filterfalse(self.is_leaf, split))

    def abstract(self):
        """ Calculate an abstract version of the tree

        Returns
        -------
        str
            a b 1 0 c 1 0 -> p0 p1 a0 a1 p2 a0 a1
        """
        abst = ""
        # this retains the order
        answer_set = list(dict.fromkeys(self.get_answers()))
        param_set = list(dict.fromkeys(self.get_parameters()))

        for node in self.word.split(" "):
            # add whitespace only after first node
            if abst:
                abst += " "
            if node in answer_set:
                abst += "a" + str(answer_set.index(node))
            elif node in param_set:
                abst += "p" + str(param_set.index(node))
            else:
                raise KeyError
        return abst
