"""
| Copyright 2017 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@tf.uni-freiburg.de>
"""

import re
import numpy as np

from coco.mpt import parser as cp
from coco.mpt import likelihood as cl

def count_occurrences(formula, param):
    """ Counts positive and negative occurrences of a given parameter in an
    MPT branch formula.

    Parameters
    ----------
    formula : str
        String representation of the branch formula. Required to contain
        whitespace between operators, e.g. 'a * (1 - b) * c'.

    param : str
        Parameter name to count occurrences of.

    Returns
    -------
    pos : int
        Number of positive occurrences.

    neg : int
        Number of negative occurrences.

    Examples
    --------
    >>> count_occurrences('a * (1 - b) * c', 'a')
    (1, 0)
    >>> count_occurrences('(1 - a) * b * (1 - a) * a', 'a')
    (1, 2)

    """

    pos = 0
    neg = 0

    # Iterate over all negative clauses '(1 - X)' where X is a
    # param and increment negative occurrences whenever X equals
    # the current parameter.
    # Simultaneously, reduce the branch formula to finally only
    # contain positive information.
    pos_rest = formula
    matches = list(re.finditer(r"\(1 - ([a-zA-Z0-9_]+)\)", formula))
    for neg_match in reversed(matches):
        if neg_match.group(1) == param:
            neg += 1

        neg_span = neg_match.span(0)
        pos_rest = pos_rest[:neg_span[0]] + pos_rest[neg_span[1]:]

    # Iterate over positive parameters and update the counters
    # whenever the current parameter is encountered.
    for pos_match in re.findall("[a-zA-Z1-9_]+", pos_rest):
        if pos_match == param:
            pos += 1

    return pos, neg

def mstep(assignment, cat_formulae, branch_frequencies):
    """ Maximization step of the EM algorithm. Computes new parameter estimates
    based on branch formulae and frequencies.

    Parameters
    ----------
    assignment : dict(str, float)
        Dictionary containing parameter names and estimates as key and values,
        respectively.

    formulae : list
        List of category formulae.

    branch_frequencies : list
        Frequencies of branch observations obtained from the E-step.

    Returns
    -------
    dict(str, float)
        Parameter assignment dictionary.

    Examples
    --------
    >>> assignment = {'g': 0.5, 'do': 0.8, 'dn': 0.7}
    >>> f = ['do + (1 - do) * g', '(1 - do) * (1 - g)', '(1 - dn) * g', 'dn + (1 - dn) * (1 - g)']
    >>> freq = np.array([8.88888889, 1.11111111, 2, 3, 9.88235294, 2.11764706])
    >>> res = mstep(assignment, f, freq)
    >>> ["{}: {:.4f}".format(key, value) for key, value in sorted(res.items())]
    ['dn: 0.6588', 'do: 0.7407', 'g: 0.4996']

    """

    new_assignment = {}

    # Retrieve the branch formulae
    branch_formulae = []
    for cat_formula in cat_formulae:
        branch_formulae.extend(cp.get_branch_formulae(cat_formula))

    # Iterate over parameters
    for param in assignment:
        # print("Param:", param)

        # Iterate over outcome categories
        acc_positive = 0
        acc_total = 0
        for branch_idx, branch_formula in enumerate(branch_formulae):
            # Retrieve the corresponding branch frequency
            branch_frequency = branch_frequencies[branch_idx]

            # Extract the number of positive and negative istances of each
            # parameter.
            pos_occurrences, neg_occurrences = count_occurrences(branch_formula, param)

            # Append to the accumulators
            acc_positive += pos_occurrences * branch_frequency
            acc_total += (pos_occurrences + neg_occurrences) * branch_frequency

            # Debugging prints
            # print("   Branch formula ({}): {}".format(branch_idx, branch_formula))
            # print("      Pos occurrences ({}): {}".format(param, pos_occurrences))
            # print("      Neg occurrences ({}): {}".format(param, neg_occurrences))
            # print("      -> acc pos:", pos_occurrences * branch_frequency)
            # exit()

        # Divide positive and total accumulators
        # print("Param", param)
        # print("   Pos:", acc_positive)
        # print("   Tot:", acc_total)
        # print()

        if acc_positive == 0:
            new_assignment[param] = 0
        else:
            new_param_value = acc_positive / acc_total
            new_assignment[param] = new_param_value

    return new_assignment

def estep(assignment, cat_formulae, cat_frequencies):
    """ Expectation step. Uses the parameter estimates obtained from the M step
    in order to update the expectation for the proceeding M step.

    Parameters
    ----------
    assignment : dict(str, float)
        Dictionary containing parameter names and estimates as key and values,
        respectively.

    formulae : list
        List of category formulae.

    cat_frequencies : list
        Frequencies of category observations.

    Returns
    -------
    list
        List of branch frequency estimates.

    Examples
    --------
    >>> assignment = {'g': 0.5, 'do': 0.8, 'dn': 0.7}
    >>> f = ['do + (1 - do) * g', '(1 - do) * (1 - g)', '(1 - dn) * g', 'dn + (1 - dn) * (1 - g)']
    >>> freq = np.array([10, 2, 3, 12])
    >>> res = estep(assignment, f, freq)
    >>> ["{:.4f}".format(x) for x in res]
    ['8.8889', '1.1111', '2.0000', '3.0000', '9.8824', '2.1176']

    """

    branch_freqs = []

    # Iterate over outcome classes
    for cat_idx, cat_formula in enumerate(cat_formulae):
        cat_prob = cl.eval_formula(cat_formula, assignment)
        cat_freq = cat_frequencies[cat_idx]
        branch_formulae = cp.get_branch_formulae(cat_formula)

        # Iterate over branches
        for branch_formula in branch_formulae:
            # Compute the branch probability
            prob = cl.eval_formula(branch_formula, assignment)

            # Compute the new branch frequency estimate
            if prob == 0:
                branch_freqs.append(0)
            else:
                freq_estimate = cat_freq * prob / cat_prob
                branch_freqs.append(freq_estimate)

    # Sanity check
    assert np.isclose(np.sum(branch_freqs), np.sum(cat_frequencies)), \
        "ERROR: Branch frequencies do not sum up to total number of " \
        "observations ({} != {}): {}".format(
            np.sum(branch_freqs), np.sum(cat_frequencies), branch_freqs)
    return np.array(branch_freqs)
