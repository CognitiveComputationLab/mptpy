""" Fitter Implementation using the Expectation Maximization Algorithm

"""

from mptpy.fitting import fitter


def fit_mpt(mpt, n_optim, use_fia=False):
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
