""" Wrapper class for MPTinR.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

from collections import OrderedDict
import numpy as np

from fitting.fitter import Fitter
import fitting.optimize as optim
import fitting.likelihood as lh


FUNCS = {"rmse" : optim.optim_rmse, "llik" : optim.optim_llik}


class ScipyFitter(Fitter):
    """ Tree fitting using SciPy """

    def __init__(self, data_path, sep=',', func="rmse", header=None):
        super().__init__(data_path, sep=sep, header=header)
        self.func = func

    def fit_mpt(self, mpt, n_optim=10, use_fia=False):
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
        # TODO what to do with restricted parameters?

        """
        if mpt.prefix_tree is not None:
            # the model consists of several subtrees, create restriction files
            self._clear_temp_dir("temp/")
            self._compute_parameter_ratios(mpt, "temp/")
        """

        kwargs = self._setup_args(mpt)

        res, errs = optim.fit_classical(**kwargs, n_optim=n_optim)

        params = kwargs['param_names']
        cat_formulae = kwargs['cat_formulae']
        data = kwargs['data']

        # Compute the correct criteria (without ignoring factorials)
        ass = dict(zip(params, res.x))
        llik = lh.log_likelihood(cat_formulae, ass, data, ignore_factorials=False)
        aic = -2 * llik + 2 * len(params)
        bic = -2 * llik + np.log(data.sum()) * len(params)

        # Compute the RMSE
        probs = np.array([lh.eval_formula(f, ass) for f in cat_formulae])
        preds = probs * data
        rmse = np.sqrt(np.mean((preds - data) ** 2))

        result = {
            'n_params': len(params),
            'n_datasets': len(data),
            'func_min': res.fun,
            'LogLik': llik,
            'AIC': aic,
            'BIC': bic,
            'RMSE': rmse,
            'OptimErrorRatio': errs * 100,
            'ParamAssignment': ass
        }

        return result

    def _setup_args(self, mpt):
        """ Compute the arguments needed for the fitting

        Parameters
        ----------
        mpt : MPT
            MPT to be fitted

        Returns
        -------
        dict
        """
        kwargs = {}
        kwargs['fun'] = FUNCS[self.func]

        data = np.array(self.read_data()[0])
        kwargs['data'] = data

        restricted = self._compute_parameter_ratios(mpt, data)

        # get class formulae
        formulae, classes = mpt.get_formulae()
        cat_formulae = {}
        for idx, cl in enumerate(classes):
            if cl not in cat_formulae.keys():
                cat_formulae[cl] = formulae[idx]
            else:
                cat_formulae[cl] += " + " + formulae[idx]

        ordered = OrderedDict(sorted(cat_formulae.items())).values()
        kwargs['cat_formulae'] = list(ordered)

        kwargs['param_names'] = list(set(mpt.word.parameters))

        return kwargs
