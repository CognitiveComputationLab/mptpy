""" Data structure for Multinomial Processing Trees (MPTs) nodes.

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""


class Node(object):
    """ Class for MPT nodes """

    def __init__(
            self,
            content,
            pos=None,
            neg=None,
            leaf=False
    ):
        self.content = content
        self.leaf = leaf
        self.pos = pos
        self.neg = neg

        print(self.content, self.leaf, self.pos, self.neg)

    def __str__(self):
        return "Node({})".format(self.content)

    def __eq__(self, other):
        pos_subtree = self.pos == other.pos
        neg_subtree = self.neg == other.neg
        return self.content == other.content and pos_subtree and neg_subtree

    def __ne__(self, other):
        return not self.__eq__(other)