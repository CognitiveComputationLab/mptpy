""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from operation import Operation


class Substitution(Operation):
    """ Parameter deletion operation on MPTs """

    def generate_candidates(self, mpt):
        """ Generate all trees possible with this operation

        Parameters
        ----------
        mpt : MPT
            mpt that is to be modified
        """

        pass
