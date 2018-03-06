""" Properties of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import re


def check(mpt, mpt_property):
    """ check for property

    Parameters
    ----------
    mpt : MPT
        MPT to be checked for property

    mpt_property : ["identifiable"]
        property to be checked for

    Returns
    -------
    boolean
        truth value of the check
    """

    return globals()[mpt_property](mpt)


def identifiable(mpt):
    """ Check for identifiability

    Parameters
    ----------
    mpt : MPT
        MPT to be checked for identifiability

    Returns
    -------
    boolean
        whether tree is identifiable
    """

    free_params = [
        x for x in set(mpt.word.parameters) if not re.match(r'y\d+', x)
    ]
    return len(free_params) <= mpt.max_parameters()
