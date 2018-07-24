""" Convert an MPT model to a tikz representation.
Usage: python3 -m to_tikz <model_file> <output_file>

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import sys

from mptpy.tools.parsing import EasyParser
from mptpy.visualization.visualize_mpt import to_tikz


def run(model_file, save_file):
    """ Draw an MPT modelto the command line

    Parameters
    ----------
    file : str
        path to the model file
    """
    parser = EasyParser()
    mpt = parser.parse(model_file)
    tikz = to_tikz(mpt)
    with open(save_file, 'w') as output:
        output.write(tikz)


if __name__ == "__main__":

    print(sys.argv)

    if len(sys.argv) < 3:
        print("Usage: python3 -m to_tikz <model_file> <output_file>")
        exit()

    run(sys.argv[1], sys.argv[2])
