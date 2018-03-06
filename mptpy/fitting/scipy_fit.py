""" Wrapper class for MPTinR.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from fitting.fitter import Fitter


class ScipyFitter(Fitter):
    """ Tree fitting using SciPy """

    def __init__(self, data_path, sep=',', header=None):
        super().__init__(data_path, sep=sep, header=header)

    def fit_mpt(self, mpt, use_fia=False):
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
        if mpt.prefix_tree is not None:
            # the model consists of several subtrees, create restriction files
            self._clear_temp_dir("temp/")
            self._compute_parameter_ratios(mpt, "temp/")
