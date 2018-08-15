""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
import itertools as it
from functools import partial
from collections import Counter
from tqdm import tqdm

from mptpy.optimization.operations.operation import Operation
from mptpy import mpt_word
from mptpy.tools import misc


DELETION_FLAG = 2


class Deletion():
    """ Parameter deletion operation on MPTs """

    def __init__(self, mpt, ignore_params=None, out='../out/out.txt'):
        if ignore_params is None:
            ignore_params = []
        self.mpt = mpt
        self.all_cats = Counter(mpt.word.answers)
        self.ignore_params = ignore_params
        self.out = out
        self.sep = self.mpt.word.sep

    def read_number(self, idx):
        with open(self.out) as trees:
            for i, line in enumerate(trees):
                if i == idx:
                    return line.strip()

    def generate_candidates(self):
        """ Generate all trees possible with this operation

        Parameters
        ----------
        mpt : MPT
            mpt that is to be modified
        """

        print("Generating deletion candidates...")

        levels = self.mpt.get_levels(self.mpt.root)

        bin_s = []
        for level in reversed(sorted(levels.keys())):
            print('\n-------------------\nLevel {}'.format(level))

            for node in levels[level]:

                bin_s.append(self.possible_subtrees(node, bin_s[:2]))
                if not node.leaf:
                    # the first two are the left-most and deepest nodes
                    bin_s = bin_s[2:]
        print("Done!")

        candidates = sorted(self.compressed(bin_s[0]), key=self.abstract)

        unique = []
        for _, group in it.groupby(candidates, key=self.abstract):
            unique.append(list(group)[0])

        f = open(self.out, 'w')
        for cand in unique:
            f.write(cand)
            f.write("\n")
        f.close()

        return unique

    def abstract(self, candidate):
        """ Calls the abstraction function of the mpt word class
        a 1 0 -> p0 1 0
        """
        word = mpt_word.MPTWord(candidate, leaf_test=self.mpt.word.is_leaf)
        return word.abstract()

    def compressed(self, binary):
        res = []
        for subtree in tqdm(binary):
            candidate = self.sep.join(
                (it.compress(str(self.mpt.root).split(self.sep), subtree)))
            res.append(candidate)
        return res

    def check_combination(self, cats_wo_node, subtree, comb):
        """ Check if the given combination for the node is okay

        Parameters
        ----------
        rem_cats : Counter
            Counter of the remaining categories in the tree using this combinatio
        """
        candidate = it.compress(subtree.split(self.sep), comb)
        cats = Counter(filter(self.mpt.word.is_leaf, candidate))
        rem_cats = cats_wo_node + cats

        return all([key in rem_cats for key in self.all_cats.keys()])

    def substitute_flag(self, comb):
        """ If the iterable contains a 'd' for delete, remove it and
        insert a 0 to the first place. Else just insert a 1.

        Parameters
        ----------
        comb : iterable

        Returns
        -------
        list
            iterable without the d and with a 0 or 1 at [0]
        """
        comb = list(comb)
        if DELETION_FLAG in comb:
            comb.remove(DELETION_FLAG)
            comb.insert(0, 0)
        else:
            comb.insert(0, 1)
        return comb

    def lazy_generation(self, check_func, left, right):
        """ Itertools variation of the generation process.

        Parameters
        ----------
        check_func : func
            (partial) function to check if the combination is possible

        left : list
            candidates for the left child

        right : list
            candidates for the right child

        Returns
        -------
        list
            all possible deletion candidates
        """

        left_candidates = left + [bytearray([0] * len(left[0]) + [2])]
        right_candidates = right + [bytearray([0] * len(right[0]) + [2])]

        candidates = it.product(left_candidates, right_candidates)

        possible = []
        total = len(left_candidates) * len(right_candidates)

        for combination in tqdm(candidates, total=total):

            combination = self.substitute_flag(
                it.chain.from_iterable(combination))
            if 2 in combination:
                continue
            if check_func(combination):
                possible.append(combination)

        return possible

    def possible_subtrees(self, node, arr_bin):
        """ Generates all possible subtrees for node.

        Parameters
        ----------
        node : Node

        arr_bin : list
            possible subtrees for left and right child

        Returns
        -------
        list
            all possible subtrees
        """

        if node.leaf or node.content in self.ignore_params:
            return [bytearray([1] * len(str(node).split(self.mpt.word.sep)))]

        cats_wo_node = self.all_cats - Counter(node.answers())
        # initialize the check function with the categories and the node
        check = partial(self.check_combination, cats_wo_node, str(node))

        return self.lazy_generation(check, arr_bin[0], arr_bin[1])
