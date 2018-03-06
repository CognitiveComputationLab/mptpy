""" Draw an MPT model to the command line.
Usage: python3 -m visualize_mpt <model_file>

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


import sys
import os

PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../mptpy'))
sys.path.insert(0, PATH)

from mpt import build_from_file


def run(file):
    """ Draw an MPT modelto the command line

    Parameters
    ----------
    file : str
        path to the model file
    """

    mpt = build_from_file(file)
    mpt.draw()
    print(mpt)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python3 -m visualize_mpt <model_file>")
        exit()

    run(sys.argv[1])
