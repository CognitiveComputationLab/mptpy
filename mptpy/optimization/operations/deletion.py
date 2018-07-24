""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


import itertools as it
from functools import partial
from queue import Queue
from collections import Counter
from collections import OrderedDict


from mptpy.optimization.operations.operation import Operation
from mptpy import mpt_word
from tqdm import tqdm


class Deletion(Operation):
    """ Parameter deletion operation on MPTs """

    def __init__(self, mpt, ignore_params=[], out='out.txt'):
        self.mpt = mpt
        self.all_cats = Counter(mpt.word.answers)
        self.is_leaf = mpt.word.is_leaf
        self.ignore_params = ignore_params
        self.out = out
        self.sep = self.mpt.word.sep
        self.deletion_flag = 2

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

        DEBUG = True

        for level in reversed(sorted(levels.keys())):
            print()
            print('-------------------')
            print()
            print("Level {}".format(level))
            print(type(bin_s))

            for node in levels[level]:

                bin_subtrees = self.generate_possible_subtrees(
                    node, bin_s[:2], DEBUG=DEBUG)
                print("returned")
                bin_s.append(bin_subtrees)
                if not node.leaf:
                    # the first two are the left-most and deepest nodes
                    bin_s = bin_s[2:]
        print("Done!")

        res = sorted(self.compressed(bin_s[0]), key=self.abstract)

        unique = []
        for _, g in it.groupby(res, key=self.abstract):
            unique.append(list(g)[0])

        self.check_for_false(unique)

        return unique

    def check_for_false(self, li):
        for candidate in li:
            cats = Counter(candidate.split(" "))
            if not all([key in cats for key in self.all_cats.keys()]):
                print("ouch")
                print(cats)
                exit()
        print("done checking for false")

    def abstract(self, candidate):
        word = mpt_word.MPTWord(candidate, leaf_test=self.is_leaf)
        return word.abstract()

    def compressed(self, binary):
        res = []
        for subtree in tqdm(binary):
            candidate = self.sep.join(
                (it.compress(str(self.mpt.root).split(self.sep), subtree)))
            res.append(candidate)
        return res

    def check_combination(self, cats_wo_node, subtree, comb, DEBUG=False):
        """ Check if the given combination for the node is okay

        Parameters
        ----------
        rem_cats : Counter
            Counter of the remaining categories in the tree using this combinatio
        """
        cats = Counter(
            filter(
                self.is_leaf,
                it.compress(
                    subtree.split(self.sep),
                    comb)))
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
        if self.deletion_flag in comb:
            comb.remove(self.deletion_flag)
            comb.insert(0, 0)
        else:
            comb.insert(0, 1)
        return comb

    def save(self, it):
        """ Write iterator to file

        Parameters
        ----------
        it : iterable
        """
        with open(self.out, 'w') as save_file:
            save_file.writelines(it)

    def help(self, it):
        return any([self.deletion_flag not in li for li in it])

    def loop_generation(self, check, left, right):
        """ Loop variation of the generation process.
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
        possible = []
        right_done = False

        for bin_left in tqdm(left):

            comb = bytearray([0]) + bin_left + bytearray([0] * len(right[0]))

            # delete right side
            if check(comb):
                possible.append(comb)

            for bin_right in right:
                if not right_done:

                    comb = bytearray([0]) + bytearray([0] *
                                                      len(left[0])) + bin_right

                    # delete left side
                    if check(comb):
                        possible.append(comb)

                comb = bytearray([1]) + bin_left + bin_right

                if check(comb):
                    possible.append(comb)

            right_done = True

        return possible

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
        i = 0
        for combination in tqdm(
                candidates,
                total=len(left_candidates) *
                len(right_candidates)):
            i += 1

            combination = self.substitute_flag(
                it.chain.from_iterable(combination))
            if 2 in combination:
                continue
            if check_func(combination):
                possible.append(combination)

        return possible

    def generate_possible_subtrees(
            self,
            node,
            arr_bin,
            DEBUG=True):
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

        if DEBUG:
            print("Generate subtrees for {}".format(node.content))

        if node.leaf or node.content in self.ignore_params:
            return [bytearray([1] * len(str(node).split(self.mpt.word.sep)))]

        cats_wo_node = self.all_cats - Counter(node.answers())
        # initialize the check function with the categories and the node
        check = partial(self.check_combination, cats_wo_node, str(node))

        return self.lazy_generation(check, arr_bin[0], arr_bin[1])
