""" Wrapper class for MPTinR.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import math
import re
from collections import OrderedDict
import numpy as np

from mptpy.fitting import fitter

from . import likelihood as lh
from . import optimize as optim


FUNCS = {"rmse": optim.optim_rmse, "llik": optim.optim_llik}


# def __init__(self, data_path, sep=',', func="rmse", header=None):
#    super().__init__(data_path, sep=sep, header=header)
#    self.func = func


def fit_easy(
        easy_file_path,
        data_path,
        func,
        sep=',',
        n_optim=10,
        use_fia=False):
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
    cat_formulae = [formula.strip().split(" #")[0]
                    for formula in cat_formulae]
    easy.close()

    # find all parameters
    pattern = re.compile(r"[A-z_]+\d*")
    params = []
    for line in cat_formulae:
        params.extend(pattern.findall(line))
    params = list(set(params))

    # setup kwargs and fit
    kwargs = _setup_args(cat_formulae, params, func, data_path, sep)
    static_params = dict()
    if len(mpt.subtrees) > 1:
        static_params = fitter.compute_parameter_ratios(mpt, fitter.read_data(data_path))
    return _fit(kwargs, static_params, n_optim=n_optim)


def fit_mpt(mpt, func, data_path, sep=',', n_optim=10, use_fia=False):
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
    static_params = dict()
    if len(mpt.subtrees) > 1:
        print("kjfdsuhiudshfi")
        static_params = fitter.compute_parameter_ratios(mpt, fitter.read_data(data_path))

    cat_formulae = _get_cat_formulae(mpt)

    params = list(set(mpt.word.parameters))
    kwargs = _setup_args(cat_formulae, params, func, data_path, sep)
    return _fit(kwargs, static_params, n_optim=n_optim)


def _fit(kwargs, static_params, n_optim=10):
    """ Fit the model

    Parameters
    ----------
    kwargs : dict
        func, data, cat_formulae, param_names

    """

    res, errs = optim.fit_classical(**kwargs, static_params=static_params, n_optim=n_optim)
    print(res)

    # Compute the correct criteria (without ignoring factorials)
    measures = _compute_measures(res, kwargs, static_params)

    # Compute the RMSE
    rmse = _rmse(measures['ass'], kwargs)

    result = {
        'n_params': len(kwargs['param_names']),
        'n_free_params' : measures['free_params'],
        'n_datasets': len(kwargs['data']),
        'func_min': res.fun,
        'LogLik': measures['llik'],
        'LogLik-R': measures['llik-r'],
        'AIC': measures['aic'],
        'BIC': measures['bic'],
        'AIC-R': measures['aic-r'],
        'BIC-R': measures['bic-r'],
        'RMSE': rmse,
        'G2' : measures['G2'],
        'OptimErrorRatio': errs * 100,
        'ParamAssignment': measures['ass']
    }

    return result


def _compute_measures(res, kwargs, static_params):
    """ Compute the correct criteria (without ignoring factorials)
    """
    data = kwargs['data']
    formulae = kwargs['cat_formulae']
    params = kwargs['param_names']
    free_params = [x for x in params if x not in static_params]
    measures = {}
    measures['ass'] = dict(zip(free_params, res.x))
    measures['ass'].update(static_params)
    measures['llik'] = lh.log_likelihood(
        formulae, measures['ass'], data, ignore_factorials=False)
    measures['llik-r'] = lh.log_likelihood(
        formulae, measures['ass'], data, ignore_factorials=True)
    measures['aic'] = -2 * measures['llik'] + 2 * len(free_params)
    measures['bic'] = -2 * measures['llik'] + \
        np.log(data.sum()) * len(free_params)
    
    measures['G2'] = _g2(data, formulae, measures['ass'])
    measures['aic-r'] = measures['G2'] + 2* len(free_params)
    measures['bic-r'] = measures['G2'] + np.log(data.sum()) * len(free_params)
    measures['free_params'] = len(free_params)

    return measures

def _g2(data, formulae, assignment):

    probs = np.array([lh.eval_formula(x, assignment) for x in formulae])

    assert math.isclose(np.sum(probs), 1)

    g2 = 2 * np.sum(data * np.log(data / (data.sum() * probs)))
    return g2

def _rmse(ass, kwargs):
    """ Compute the RMSE

    Parameters
    ----------
    ass : dict
        Parameter Assignment

    kwargs : dict

    """
    probs = np.array([lh.eval_formula(f, ass)
                      for f in kwargs['cat_formulae']])
    preds = probs * kwargs['data']
    rmse = np.sqrt(np.mean((preds - kwargs['data']) ** 2))
    return rmse


def _get_cat_formulae(mpt):
    """ Retrieve categories and respective formulae

    Parameters
    ----------
    mpt : MPT
        model

    """

    values = []
    for _, value in mpt.formulae().items():
        values.append(" + ".join(value))

    return values


def _setup_args(cat_formulae, params, func, data_path, sep=','):
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
    kwargs['fun'] = FUNCS[func]

    data = np.array(fitter.read_data(data_path, sep))
    kwargs['data'] = data

    #ed = self._compute_parameter_ratios(mpt, data)

    kwargs['cat_formulae'] = cat_formulae

    kwargs['param_names'] = sorted(params)

    return kwargs
