""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from abc import ABCMeta, abstractmethod


class Operation(object):
    """ Base class for operations on MPTs """
    __metaclass__ = ABCMeta

    @abstractmethod
    def generate_candidates(self, mpt):
        """ Generate all trees possible with this operation

        Parameters
        ----------
        mpt : MPT
            mpt that is to be modified
        """
        pass

    @abstractmethod
    def apply(self, mpt):
        pass
