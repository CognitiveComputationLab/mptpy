""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


from itertools import product, chain, compress
from functools import partial
from queue import Queue
from collections import Counter

from mptpy.optimization.operations.operation import Operation
from tqdm import tqdm


def merge_dicts(*dicts):
    """ Merge two dictionaries
    example: merge({1:'a', 2:'b'}, {1:'c'}) -> {1:['a','c'], 2:['c']}

    Parameters
    ----------
    dicts
        Dictionaries to be merged
    """
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

    def __init__(self, mpt, out='out.txt'):
        self.mpt = mpt
        self.all_cats = Counter(mpt.word.answers)
        self.is_leaf = mpt.word.is_leaf
        self.out = out

    def generate_candidates(self):
        """ Generate all trees possible with this operation

        Parameters
        ----------
        mpt : MPT
            mpt that is to be modified
        """

        print("Generating deletion candidates...")

        levels = self.get_levels()

        bin_s = []

        DEBUG = True

        for level in reversed(sorted(levels.keys())):
            print()
            print('-------------------')
            print()
            print("Level {}".format(level))

            for node in levels[level]:

                bin_subtrees = self.generate_possible_subtrees(node, bin_s[:2], DEBUG=DEBUG)
                bin_s.append(bin_subtrees)
                if not node.leaf:
                    bin_s = bin_s[2:] # the first two are the left-most and deepest nodes
        print("Done!")

        res = []
        for subtree in bin_s[0]:
            candidate = " ".join((compress(str(self.mpt.root).split(" "), subtree)))
            if candidate not in res:
                res.append(candidate)

        f = open(self.out, 'w')
        f.writelines(res)
        f.close()
        return res

    def check_combination(self, cats_wo_node, subtree, comb, DEBUG=False):
        """ Check if the given combination for the node is okay

        Parameters
        ----------
        rem_cats : Counter
            Counter of the remaining categories in the tree using this combinatio
        """
        cats = Counter(filter(self.is_leaf, compress(subtree.split(" "), comb)))
        rem_cats = cats_wo_node + cats
        if all([key in rem_cats for key in self.all_cats.keys()]):

            return True

        return False

    def substitute_d(self, comb):
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
        if 'd' in comb:
            comb.remove('d')
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
        
        left_candidates  = left  + [[0] * len(left[0]) + ["d"]]
        right_candidates = right + [[0] * len(right[0]) + ["d"]]

        candidates = product(left_candidates, right_candidates)

        possible = []
        i = 0
        for combination in tqdm(candidates, total=len(left_candidates) * len(right_candidates)):
            i += 1
            """
            if i == 1000000:
                out_file = open(self.out, 'w')
                out_file.writelines(possible)
                out_file.close()

                possible.clear()
                i = 0
            """
            combination = self.substitute_d(chain.from_iterable(combination))
            if 'd' in combination:
                continue
            if check_func(combination):
                possible.append(combination)

        return possible

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

            comb = [0] + bin_left + [0] * len(right[0])

            # delete right side
            if check(comb):
                possible.append(comb)

            for bin_right in right:
                if not right_done:

                    comb = [0] + [0] * len(left[0]) + bin_right

                    # delete left side
                    if check(comb):
                        possible.append(comb)
                
                comb = [1] + bin_left + bin_right

                if check(comb):
                    possible.append(comb)
            
            right_done = True

        return possible



    def generate_possible_subtrees(self, node, arr_bin, ignore_params=[], DEBUG=True):
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

        if node.leaf:
            return [[1]]

        if node.content in ignore_params:
            return [[1] * len(str(node).split(self.mpt.word.sep))]

        cats_wo_node = self.all_cats - Counter(node.answers())
        check = partial(self.check_combination, cats_wo_node, str(node))

        lazy = True

        if lazy:
            return self.lazy_generation(check, arr_bin[0], arr_bin[1])

        else:
            return self.loop_generation(check, arr_bin[0], arr_bin[1])


    def get_levels(self, node=None, level=0):
        """ Generate a dict with all nodes and their respective level
        0 is the root

        Parameters
        ----------
        node : Node, optional
            if None, will take the root

        level : int, optional
            level from which to start counting
        """       
        if node is None:
            node = self.mpt.root

        levels = {level: [node]}
        
        if not node.leaf:
            left_dict  = self.get_levels(node.pos, level=level + 1)
            right_dict = self.get_levels(node.neg, level=level + 1)

            temp = merge_dicts(left_dict, right_dict)
            
            levels.update(temp)

        return levels
