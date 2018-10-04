""" Optimization procedures for MPTs.

"""

from collections import Counter
import os
import sys

import numpy as np
from sympy.combinatorics.partitions import RGS_enum

from mptpy.optimization.operations.deletion import Deletion
import mptpy.optimization.operations.substitution as substitution
from mptpy.mpt_word import MPTWord
from mptpy.mpt import MPT
import mptpy.fitting.scipy_fit as fitting
import mptpy.properties.properties as props


class Optimizer():
    def __init__(self, mpt, data_path, name, sep=',', func='rmse',
                 ignore_params=None):
        if ignore_params is None:
            ignore_params = []
        self.mpt = mpt
        self.deletion_file = 'delete_{}.txt'.format(name)
        self.deletion = Deletion(
            mpt,
            ignore_params=ignore_params,
            out=self.deletion_file)
        self.ignore_params = ignore_params
        self.eval_file = 'evals_{}.txt'.format(name)
        self.data_path = data_path
        self.no_del_trees = 0
        self.func = func
        self.sep = sep

    def init_deletion(self):
        if not os.path.exists(self.deletion_file):
            deletion_trees = self.deletion.generate_candidates()
            self.no_del_trees = len(deletion_trees) - 1
        else:
            print("Deletion list exists. Load..")
            sys.stdout.flush()
            self.no_del_trees = sum(1 for line in open(self.deletion_file))

    def random_search(self):

        evaluation = fitting.fit_mpt(
            self.mpt, self.func, self.data_path, sep=self.sep)
        from pprint import pprint
        pprint(evaluation)
        exit()
        self.write_to_file(str(self.mpt), evaluation)

        i = 0
        while(1):
            i += 1
            print("Optimizing {}...".format(i))
            model, evaluation = self.eval_random_model(self.mpt.subtrees)
            if model:
                self.write_to_file(str(model), evaluation)


    def eval_random_model(self, subtrees):
        # deletion
        del_tree = self.random_deletion_model()

        # substitutions
        param_rgs = self.random_substitution_configs(del_tree)

        subst = substitution.Substitution(param_rgs)
        model = MPT(subst.apply(del_tree))
        model.subtrees = subtrees

        if props.check(model, 'identifiable'):

            evaluation = fitting.fit_mpt(
                model, self.func, self.data_path, sep=self.sep)
            print(str(model))
            print(evaluation)
            print()
            sys.stdout.flush()
            return str(model), evaluation

        return None, None


    def random_substitution_configs(self, model):
        param_nos = Counter(model.parameters)
        rand_perm = {param: np.random.randint(0, RGS_enum(param_nos[param])) for param in param_nos}

        param_rgs = {}
        for param in rand_perm.keys():
            rand = rand_perm[param]
            param_count = param_nos[param]

            if param in self.ignore_params:
                rgs = [0] * param_count
            else:
                rgs = substitution.get_RGS(rand, param_count)
            param_rgs[param] = rgs
        return param_rgs


    def random_deletion_model(self):
        deletion_no = np.random.randint(0, self.no_del_trees)
        del_tree = self.deletion.read_number(deletion_no)

        del_tree = MPTWord(
            del_tree,
            sep=self.mpt.word.sep,
            leaf_test=self.mpt.word.is_leaf)

        return del_tree


    def write_to_file(self, model, evaluation):
        with open(self.eval_file, 'a') as out_file:
            out_file.write(" ".join([model, str(evaluation)]))
            out_file.write("\n")
