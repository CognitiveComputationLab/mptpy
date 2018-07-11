""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from mptpy.optimization.operations.operation import Operation
from queue import Queue
from collections import Counter


def merge_dicts(*dicts):
    temp = {}

    for d in (dicts):
        
        for key, value in d.items():
            if key in temp.keys():
                temp[key].extend(value)
            else:
                temp[key] = value
    return temp



class Deletion(Operation):
    """ Parameter deletion operation on MPTs """

    def __init__(self, mpt):
        self.mpt = mpt
        self.word = mpt.word
        self.all_cats = mpt.word.answers
        self.nodes = []
        self.is_leaf = self.word.is_leaf

    def generate_candidates(self):
        """ Generate all trees possible with this operation

        Parameters
        ----------
        mpt : MPT
            mpt that is to be modified
        """

        levels = self.get_levels()

        arr = []

        for level in reversed(sorted(levels.keys())):
            for node in levels[level]:
                
                arr.append(self.generate_possible_subtrees(node, arr))
                if not node.leaf:
                    arr = arr[2:]
        return arr[0]

    def check_combination(self, combination, node):
        cats = Counter(filter(self.is_leaf, combination))
        rem_cats = Counter(self.all_cats) - Counter(node.answers()) + Counter(cats)

        if all([key in rem_cats for key in Counter(self.all_cats).keys()]):
            return True
        return False


    def generate_possible_subtrees(self, node, arr):

        if node.leaf:
            return [node.content]
        poss = []

        # both kept
        for left in arr[0]:
            # delete right side
            if left not in poss and self.check_combination(left, node):
                poss.append(left)  
            for right in arr[1]:
                # delete left side
                if right not in poss and self.check_combination(right, node):
                    poss.append(right)
                
                # keep both sides
                p = " ".join([node.content, left, right])
                if p not in poss and self.check_combination(p, node):
                    poss.append(p)

        return poss

    def get_levels(self, node=None, level=0):        
        
        if node is None:
            node = self.mpt.root

        levels = {level: [node]}
        
        if not node.leaf:
            left_dict  = self.get_levels(node.pos, level=level + 1)
            right_dict = self.get_levels(node.neg, level=level + 1)

            temp = merge_dicts(left_dict, right_dict)
            
            levels.update(temp)

        return levels
