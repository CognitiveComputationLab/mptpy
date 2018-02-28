""" Interface for the fitting and evaluation of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from abc import ABCMeta, abstractmethod


class Fitter(object):
    """ Interface class for a tree fitting module """
    __metaclass__ = ABCMeta

    @abstractmethod
    def fit_mpt(self, tree_path, data_path, use_fia):
        """ Fit the tree and return all metrics """
        pass
