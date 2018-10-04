""" Script containing functions related to the optimization of MPTs.

"""

import numpy as np
from scipy.optimize import minimize

from . import likelihood as lh


def optim_llik(param_values, cat_formulae, param_names, data, static_params):
    """ Realizes an objective function based on the log likelihood value of a
    parameterized MPT model.

    Parameters
    ----------
    param_values : list(float)
        List of parameter values.

    cat_formulae : list(str)
        List of category formula strings.

    param_names : list(str)
        List of parameter identifier strings.

    data : ndarray
        Data array.

    Returns
    -------
    float
        Likelihood value of the parameterized model and given data.

    Examples
    --------
    >>> param_values = [0.5]
    >>> cat_formulae = ['a', '(1 - a)']
    >>> param_names = ['a']
    >>> data = np.array([10, 10])
    >>> optim_llik(param_values, cat_formulae, param_names, data)
    13.862943611198906
    >>> data = np.array([20, 10])
    >>> optim_llik(param_values, cat_formulae, param_names, data)
    20.794415416798358

    """

    # Construct the assignment dictionary
    ass = dict(zip(param_names, param_values))
    assert not np.any([x in ass for x in static_params.keys()]), \
        'Static parameter found in constructed assignment dictionary.'
    ass.update(static_params)

    llik = lh.log_likelihood(cat_formulae, ass, data, ignore_factorials=True)
    return -1 * llik


def optim_rmse(param_values, cat_formulae, param_names, data):
    """ Realizes an objective function based on the Root-Mean-Squared Error
    between a models predictions (i.e. probabilities times number of
    occurrences) and true observations.

    Parameters
    ----------
    param_values : list(float)
        List of parameter values.

    cat_formulae : list(str)
        List of category formula strings.

    param_names : list(str)
        List of parameter identifier strings.

    data : ndarray
        Data array.

    Returns
    -------
    float
        RMSE value between the true observations and model predictions.

    Examples
    --------
    >>> param_values = [0.5]
    >>> cat_formulae = ['a', '(1 - a)']
    >>> param_names = ['a']
    >>> data = np.array([10, 10])
    >>> optim_rmse(param_values, cat_formulae, param_names, data)
    0.0
    >>> data = np.array([20, 10])
    >>> optim_rmse(param_values, cat_formulae, param_names, data)
    5.0

    """

    # Construct the assignment dictionary
    ass = dict(zip(param_names, param_values))

    # Compute the individual RMSE values
    cat_probs = np.array([lh.eval_formula(f, ass) for f in cat_formulae])
    preds = data.sum() * cat_probs
    return np.sqrt(np.mean((preds - data) ** 2))


def fit_classical(fun, cat_formulae, free_params, static_params, data, n_optim=10):
    """ Fits an MPT model using classical function-based optimization routines
    implemented in the Scipy module.

    Parameters
    ----------
    fun : function
        Function to be optimized (e.g. optim_llik or optim_rmse).

    cat_formulae : list(str)
        List of MPT category formulae.

    param_names : list(str)
        List of parameter identifier strings.

    data : ndarray
        Data array.

    n_optim : int
        Number of optimization attemts (in order to alleviate the problem of
        running into local minima). In case of convergence errors, the runs are
        not repeated.

    Returns
    -------
    scipy.optimize.OptimizeResult
        Optimization result of the best fitting run (minimum function
        evaluation).

    float
        Ratio of erroneous optimization runs (e.g. due to convergence problems)
        reported as number of failed runs divided by the number of all runs.

    Examples
    --------

    >>> cat_formulae = ['a', '(1 - a)']
    >>> param_names = ['a']
    >>> data = np.array([20, 10])
    >>> res, _ = fit_classical(optim_llik, cat_formulae, param_names, data)
    >>> res.x
    array([ 0.66666666])
    >>> res, _ = fit_classical(optim_rmse, cat_formulae, param_names, data)
    >>> res.x
    array([ 0.66666666])

    """

    best_res = None
    n_errs = 0
    for _ in range(n_optim):
        # Initialize the parameter set
        init_params = np.random.uniform(0.01, 0.99, size=(len(free_params),))

        # Perform the optimization
        res = minimize(
            fun=fun,
            x0=init_params,
            args=(cat_formulae, free_params, data, static_params),
            method='L-BFGS-B',
            bounds=[(0.000001, 0.999999)] * len(init_params))

        # In case of success, compare the result with the best observed so far
        # and update if better.
        if res.success:
            if not best_res or best_res.fun > res.fun:
                best_res = res
        else:
            n_errs += 1

    return best_res, n_errs / n_optim
