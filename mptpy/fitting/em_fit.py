""" Fitter Implementation using the Expectation Maximization Algorithm

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from fitter import Fitter


class EMFitter(Fitter):
    """ Tree fitting using the EM algorithm """

    def fit_mpt(self, tree_path, data_path, use_fia=False):
        """ Fit the given tree with the EM algorithm

        Parameters
        ----------
        tree_path : str
            Path to the tree file in the easy format

        data_path : str
            Path to the data

        use_fia : boolean, optional
            wether FIA is wished to be used.
            Default: False.

        Returns
        -------
        dict
            BIC, GSQ, Likelihood (and optionally FIA)

        """

        raise NotImplementedError