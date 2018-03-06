""" Script containing functions related to the optimization of MPTs.

| Copyright 2017 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@tf.uni-freiburg.de>

"""

import time

import numpy as np
from scipy.optimize import minimize

from coco.mpt import em as ce
from coco.mpt import likelihood as cl
from coco.mpt import parser as cp

def run_optimization(
        cat_formulae, observations,
        starting_assignment=None, max_iterations=None, print_logs=False,
        ignore_factorials=False):
    """ Executes the EM algorithm to optimize parameters with respect to the
    logarithmic likelihood of an MPT model.

    Parameters
    ----------
    cat_formulae : list(str)
        List of strings containing the formulae for the MPT categories.

    observations : list(int)
        List of integers representing the category observations.

    starting_assignment : dict, optional
        Dictionary containing key/value pairs of parameters and initial
        assignments, respectively.

    max_iterations : int, optional
        Number of maximum iterations. None, if the algorithm should be forced
        to run until convergence.

    print_logs : Boolean, optional
        True, if logs per epoch (likelihood, assignment, branch frequencies)
        are to be printed. False, otherwise.

    Returns
    -------
    assignments : dict
        Dictionary containing key-value pairs of parameters and final
        estimates, respectively.

    log_likelihoods : list(float)
        List of log likelihoods encountered during the optimization procedure.

    """

    # Initialize the algorithm
    params = cp.extract_params(cat_formulae)
    ass = starting_assignment
    if not ass:
        #pylint: disable=no-member
        values = np.random.uniform(size=(len(params),))
        #pylint: enable=no-member
        ass = dict(zip(params, values))
    branch_freq_estimates = None

    it_counter = 1
    log_likelihoods = []

    # Iteratively optimize the parameter assignments until convergence is
    # reached or the maximum number of iterations exceeded.
    while not max_iterations or it_counter < max_iterations:
        # Start timer for this iteration
        start = time.time()

        # Perform the expectation and maximization steps
        branch_freq_estimates = ce.estep(ass, cat_formulae, observations)
        ass = ce.mstep(ass, cat_formulae, branch_freq_estimates)

        # Compute the current likelihood
        lik = cl.log_likelihood(
            cat_formulae,
            ass,
            observations,
            ignore_factorials=ignore_factorials)

        log_likelihoods.append(lik)

        if len(log_likelihoods) >= 2 and np.abs(
                log_likelihoods[-1] - log_likelihoods[-2]) < 1e-9:
            break

        if print_logs:
            print("Iteration {} (took {:.2f}s)...".format(
                it_counter, time.time() - start))
            print("   Likelihood:", lik)
            # print("   New assignment:", ass)
            # print("   New branch_freq_estimates:", branch_freq_estimates)
            print()
        it_counter += 1

    return ass, log_likelihoods

def optim_llik(param_values, cat_formulae, param_names, data):
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
    llik = cl.log_likelihood(cat_formulae, ass, data, ignore_factorials=True)
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
    cat_probs = np.array([cl.eval_formula(f, ass) for f in cat_formulae])
    preds = data.sum() * cat_probs
    return np.sqrt(np.mean((preds - data) ** 2))

def fit_classical(fun, cat_formulae, param_names, data, n_optim=10):
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
        init_params = np.random.uniform(0.01, 0.99, size=(len(param_names),))

        # Perform the optimization
        res = minimize(
            fun=fun,
            x0=init_params,
            args=(cat_formulae, param_names, data),
            method='L-BFGS-B',
            bounds=[(0.01, 0.99)] * len(init_params))

        # In case of success, compare the result with the best observed so far
        # and update if better.
        if res.success:
            if not best_res or best_res.fun > res.fun:
                best_res = res
        else:
            n_errs += 1

    return best_res, n_errs / n_optim
