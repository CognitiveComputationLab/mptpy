""" Module for visualizations of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

def to_tikz(mpt, code_path):
    """ Generate tikz code for given MPT
    Parameters
    ----------
    mpt : MPT
        MPT to be translated to tikz

    code_path : str
        specify where to save the tikz code
    """

    raise NotImplementedError


def cmd_draw(mpt):
    """ Draw the mpt to the command line

    Parameters
    ----------
    mpt : MPT
        MPT to be drawn
    """

    raise NotImplementedError
