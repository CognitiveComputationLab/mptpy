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
            neg=None
    ):
        self.content = content
        self.pos = pos
        self.neg = neg

    @property
    def leaf(self):
        return self.pos is None 

    def __len__(self):
        """ Number of nodes in the subtree where the
        current node is the root (including this node itself)
        
        Returns
        -------
        int
            number of nodes
        """
        if self.leaf:
            return 1
        else:
            return 1 + len(self.pos) + len(self.neg)



    def __str__(self):
        return "Node({})".format(self.content)

    def __eq__(self, other):
        pos_subtree = self.pos == other.pos
        neg_subtree = self.neg == other.neg
        return self.content == other.content and pos_subtree and neg_subtree

    def __ne__(self, other):
        return not self.__eq__(other)
