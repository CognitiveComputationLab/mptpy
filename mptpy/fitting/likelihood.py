""" Script containing functions related to the likelihood computation.

| Copyright 2017 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@tf.uni-freiburg.de>

"""

import numpy as np


def eval_formula(formula, assignment):
    """ Evaluates a formula represented as a string.

    **Attention**: Be extremely careful about what to pass to this function.
    All parameters are plugged into the formula and evaluated using `eval()`
    which executes arbitrary python code.

    Parameters
    ----------
    formula : str
        String representation of the formula to be evaluated.

    assignment : dict
        Dictionary containing parameter names and values as keys and values,
        respectively.

    Returns
    -------
    float
        Evaluation result.

    Examples
    --------
    >>> eval_formula('a + (1 - b) * a', {'a': 0.1, 'b': 0.8})
    0.12
    """

    expression = formula
    for param, value in sorted(assignment.items(), reverse=True):
        expression = expression.replace(param, str(value))

    # pylint: disable=eval-used
    return eval(expression)
    # pylint: enable=eval-used


def likelihood(cat_formulae, assignment, observations):
    """ Computes the likelihood for an MPT model with given category formulae
    and parameter assignments.

    Parameters
    ----------
    cat_formulae : list(str)
        List of strings representing the category formulae.

    assignment : dict
        Dictionary containing parameter names and values as keys and values,
        respectively.

    observations : list
        List containing numbers of observations per category.

    Returns
    -------
    float
        Likelihood of the model.

    Examples
    --------
    >>> f = ['do + (1 - do) * g', '(1 - do) * (1 - g)', '(1 - dn) * g', 'dn + (1 - dn) * (1 - g)']
    >>> assignment = {'do': 0.2, 'dn': 0.4, 'g': 0.5}
    >>> observations = [15, 5, 3, 10]
    >>> likelihood(f, assignment, observations)
    9332616.569797233

    """

    # Check the input
    assert len(cat_formulae) == len(observations)

    # Evaluate the formulae
    cat_probs = []
    for cat_formula in cat_formulae:
        cat_probs.append(eval_formula(cat_formula, assignment))
    cat_probs = np.array(cat_probs)

    # Compute the likelihood
    factorials = np.array([np.math.factorial(x) for x in observations])
    n_observations = np.sum(observations)
    return np.math.factorial(n_observations) * np.prod(
        cat_probs ** observations / factorials)


def log_factorial(val):
    """ Computes the logarithmic factorial log(val!).

    Parameters
    ----------
    val : int
        Number for which the factorial is to be computed.

    Returns
    -------
    int
        log(val!)

    Examples
    --------
    >>> "{:.4f}".format(log_factorial(10))
    '15.1044'

    """

    # pylint: disable=no-member
    return np.log(np.arange(1, val + 1)).sum()
    # pylint: enable=no-member


def log_likelihood(
        cat_formulae, assignment, observations, ignore_factorials=False):
    """ Computes the logarithmic likelihood of the MPT model.

    Parameters
    ----------
    cat_formulae : list(str)
        List of strings representing the category formulae.

    assignment : dict
        Dictionary containing parameter names and values as keys and values,
        respectively.

    observations : list
        List containing numbers of observations per category.

    ignore_factorials : Boolean, optional
        Flag indicating the inclusion or ignorance of the factorial constants.
        Setting this to True results in the same behaviour as MPTinR.

    Returns
    -------
    float
        Likelihood of the model.

    Examples
    --------
    >>> f = ['do + (1 - do) * g', '(1 - do) * (1 - g)', '(1 - dn) * g', 'dn + (1 - dn) * (1 - g)']
    >>> assignment = {'do': 0.2, 'dn': 0.4, 'g': 0.5}
    >>> observations = [15, 5, 3, 10]
    >>> res = log_likelihood(f, assignment, observations)
    >>> "{:.4f}".format(res)
    '16.0490'
    >>> np.isclose(res, np.log(likelihood(formulae, assignment, observations)))
    True

    """

    # Evaluate the formulae
    cat_probs = [eval_formula(f, assignment) for f in cat_formulae]

    observations = np.array(observations)

    # pylint: disable=no-member
    llik = np.sum(observations * np.log(cat_probs))
    if not ignore_factorials:
        # Compute the log factorials for the observations
        obs_factorials = np.sum([log_factorial(x) for x in observations])
        n_factorial = log_factorial(observations.sum())
        llik += n_factorial - obs_factorials
    # pylint: enable=no-member

    return llik
