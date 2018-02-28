""" Wrapper class for MPTinR.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from fitter import Fitter


class ScipyFitter(Fitter):
    """ Tree fitting using SciPy """

    def fit_mpt(self, tree_path, data_path, use_fia=False):
        """ Fit the given tree using SciPy

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
