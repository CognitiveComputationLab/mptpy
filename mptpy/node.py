""" Data structure for Multinomial Processing Trees (MPTs) nodes.

"""


class Node(object):
    """ Class for MPT nodes

    """

    def __init__(self, content, pos=None, neg=None):
        self.content = content
        self.pos = pos
        self.neg = neg

    @property
    def leaf(self):
        """ Whether node is leaf

        """

        return self.pos is None

    def answers(self):
        """ Reachable answer categories from this node

        Returns
        -------
        list
            Answer categories in subtree

        """

        if self.leaf:
            return [self.content]

        return self.pos.answers() + self.neg.answers()

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

        return 1 + len(self.pos) + len(self.neg)

    def __str__(self):
        if self.leaf:
            return self.content
        return self.content + " " + str(self.pos) + " " + str(self.neg)

    def __eq__(self, other):
        pos_subtree = self.pos == other.pos
        neg_subtree = self.neg == other.neg
        return self.content == other.content and pos_subtree and neg_subtree

    def __ne__(self, other):
        return not self.__eq__(other)
