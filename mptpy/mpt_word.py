""" Class module for MPTs in the BMPT language.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import string
from itertools import filterfalse
from collections import OrderedDict


class MPTWord(object):
    """ MPT in the BMPT format """

    def __init__(self, word, sep=" ", leaf_test=None):
        self.str_ = word
        self.sep = sep

        # defines what characterizes a leaf node
        if leaf_test is None:
            self.is_leaf = lambda node: all(
                [ch in string.digits for ch in node])
        else:
            self.is_leaf = leaf_test

    @property
    def answers(self):
        """ Return all the answers

        Returns
        -------
        list
            list of all the answers, with duplicates
        """
        list_ = self.str_.split(self.sep)
        return list(filter(self.is_leaf, list_))

    @property
    def parameters(self):
        """ Return all the (inner node) parameters

        Returns
        -------
        list
            list of all the parameters, with duplicates
        """
        list_ = self.str_.split(self.sep)
        return list(filterfalse(self.is_leaf, list_))

    def abstract(self):
        """ Calculate an abstract version of the tree

        Returns
        -------
        str
            a b 1 0 c 1 0 -> p0 p1 a0 a1 p2 a0 a1
        """
        abst = ""

        # this retains the order
        answer_set = list(OrderedDict.fromkeys(self.answers))
        param_set = list(OrderedDict.fromkeys(self.parameters))

        for node in self.str_.split(self.sep):
            # add whitespace only after first node
            if abst:
                abst += self.sep
            if node in answer_set:
                abst += "a" + str(answer_set.index(node))
            elif node in param_set:
                abst += "p" + str(param_set.index(node))

        return abst

    def split_pos_neg(self):
        """ Splits an MPT represented as a word from the formal MPT language
        into its positive and negative subtrees following the success edge
        (parameter probability) or failure (inverse parameter probability) edge.

        Returns
        -------
        pos_subtree : str
            String representation of the positive subtree.

        neg_subtree : str
            String representation of the negative subtree.
        """
        expected_outcomes = 1
        pos = []
        split_string = self.str_.split()
        for idx, item in enumerate(split_string[1:]):
            pos.append(item)
            if not self.is_leaf(item):
                expected_outcomes += 1
            else:
                expected_outcomes -= 1

            if expected_outcomes == 0:
                return self.sep.join(pos), self.sep.join(
                    split_string[idx + 2:])

    def __len__(self):
        return len(self.str_.split(sep=self.sep))

    def __eq__(self, other):
        return self.str_ == other.str_

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.str_

    def __add__(self, other):
        new = MPTWord(self.str_ + self.sep.join(list(other)), self.sep)
        new.is_leaf = self.is_leaf
        return new

    def __getitem__(self, idx):
        return list(self)[idx]

    def __iter__(self):
        list_ = self.str_.split(sep=self.sep)
        return iter(list_)
