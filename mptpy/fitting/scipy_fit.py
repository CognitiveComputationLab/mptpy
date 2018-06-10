""" Wrapper class for MPTinR.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re
from collections import OrderedDict
import numpy as np

from .fitter import Fitter
from . import optimize as optim
from . import likelihood as lh


FUNCS = {"rmse" : optim.optim_rmse, "llik" : optim.optim_llik}


class ScipyFitter(Fitter):
    """ Tree fitting using SciPy """

    def __init__(self, data_path, sep=',', func="rmse", header=None):
        super().__init__(data_path, sep=sep, header=header)
        self.func = func

    def fit_easy(self, easy_file_path, n_optim=10, use_fia=False):
        """ Fit the given tree using SciPy

        Parameters
        ----------
        easy_file_path : str
            Path to the tree file in the easy format

        n_optim : int, optional
            number of optimization steps

        use_fia : boolean, optional
            wether FIA is wished to be used.
            Default: False.

        Returns
        -------
        dict
            BIC, GSQ, Likelihood (and optionally FIA)

        """
        # read the file
        easy = open(easy_file_path, 'r')
        cat_formulae = easy.readlines()
        cat_formulae = [formula.strip().split(" #")[0] for formula in cat_formulae]
        easy.close()

        # find all parameters
        p = re.compile("[A-z_]+\d*")
        params = []
        for line in cat_formulae:
            params.extend(p.findall(line))
        params = list(set(params))

        # setup kwargs and fit
        kwargs = self._setup_args(cat_formulae, params)
        return self._fit(kwargs, n_optim=n_optim)      


    def fit_mpt(self, mpt, n_optim=10, use_fia=False):
        """ Fit the given tree using SciPy

        Parameters
        ----------
        mpt : MPT
            mpt model
        
        n_optim : int, optional
            number of optimization steps

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
        cat_formulae = self._get_cat_formulae(mpt)
        params = list(set(mpt.word.parameters))
        kwargs = self._setup_args(cat_formulae, params)
        return self._fit(kwargs, n_optim=n_optim)



    def _fit(self, kwargs, n_optim=10):
        """ Fit the model

        Parameters
        ----------
        kwargs : dict
            func, data, cat_formulae, param_names
        
        """
        res, errs = optim.fit_classical(**kwargs, n_optim=n_optim)

        # Compute the correct criteria (without ignoring factorials)
        measures = self._compute_measures(res, kwargs)

        # Compute the RMSE
        rmse = self._rmse(measures['ass'], kwargs)

        result = {
            'n_params': len(kwargs['param_names']),
            'n_datasets': len(kwargs['data']),
            'func_min': res.fun,
            'LogLik': measures['llik'],
            'AIC': measures['aic'],
            'BIC': measures['bic'],
            'RMSE': rmse,
            'OptimErrorRatio': errs * 100,
            'ParamAssignment': measures['ass']
        }

        return result

    def _compute_measures(self, res, kwargs):
        """ Compute the correct criteria (without ignoring factorials)
        """
        data = kwargs['data']
        formulae = kwargs['cat_formulae']
        params = kwargs['param_names']
        measures = {}
        measures['ass'] = dict(zip(params, res.x))
        measures['llik'] = lh.log_likelihood(formulae, measures['ass'], data, ignore_factorials=False)
        measures['aic'] = -2 * measures['llik'] + 2 * len(params)
        measures['bic'] = -2 * measures['llik'] + np.log(data.sum()) * len(params)
        return measures

    def _rmse(self, ass, kwargs):
        """ Compute the RMSE

        Parameters
        ----------
        ass : dict
            Parameter Assignment
        
        kwargs : dict

        """
        probs = np.array([lh.eval_formula(f, ass) for f in kwargs['cat_formulae']])
        preds = probs * kwargs['data']
        rmse = np.sqrt(np.mean((preds - kwargs['data']) ** 2))
        return rmse

    def _get_cat_formulae(self, mpt):
        """ Retrieve categories and respective formulae

        Parameters
        ----------
        mpt : MPT
            model
        
        """
        formulae, classes = mpt.get_formulae()
        cat_formulae = {}
        for idx, cl in enumerate(classes):
            if cl not in cat_formulae.keys():
                cat_formulae[cl] = formulae[idx]
            else:
                cat_formulae[cl] += " + " + formulae[idx]

        ordered = OrderedDict(sorted(cat_formulae.items())).values()
        cat_formulae = list(ordered)
        return cat_formulae


    def _setup_args(self, cat_formulae, params):
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

        #restricted = self._compute_parameter_ratios(mpt, data)

        kwargs['cat_formulae'] = cat_formulae

        kwargs['param_names'] = params

        return kwargs
