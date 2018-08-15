""" Optimize an MPT model and return the optimal model.
Usage: python3 -m optimize_mpt <model_file> <data_file>

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


import argparse
import sys

from mptpy.tools.parsing import Parser
from mptpy.optimization.optimize import Optimizer


def parse_commandlineargs():
    """ Parses the command line arguments containing user preferences regarding the optimization
    procedure (input files, number of optimizations, etc.).

    Returns
    -------
    dict(str, object)
        Dictionary containing the settings for the optimization run.

    """

    parser = argparse.ArgumentParser(
        description='Perform generic fitting operations on Multinomial' +
        'Processing Trees (MPTs).')

    # Mandatory arguments
    parser.add_argument(
        'model_path',
        metavar='model',
        type=str,
        help='Path to the MPT model specification file.')

    parser.add_argument(
        'data_path',
        metavar='data',
        type=str,
        help='Path to the data file in CSV format.')

    # Optional arguments
    n_default = 10
    parser.add_argument(
        '-n',
        '--n_optim',
        metavar='N',
        type=int,
        default=n_default,
        help='Number of fitting repetitions to evade local maxima. (Default={})'.
        format(n_default))

    s_default = ','
    parser.add_argument(
        '-s',
        '--sep',
        metavar='S',
        type=str,
        default=s_default,
        help="Data table column separator. (Default='{}')".format(s_default))

    parser.add_argument(
        '--header',
        action='store_true',
        help="Is the first not-commented line a header?")

    parser.add_argument(
        '--llik',
        action='store_true'
    )

    parser.add_argument(
        '-i',
        '--ignore',
        type=str,
        nargs='+',
        help='Set of Parameter names which are not to be modified, ALL for all \
        parameters'
    )

    args = parser.parse_args()
    return vars(args)


def run(model_path, data_path, ignore=None, sep=',', header=None, n_optim=10, llik=False):
    """ Draw an MPT modelto the command line

    Parameters
    ----------
    file : str
        path to the model file
    data : str
        path to the data file
    """
    parser = Parser()
    mpt = parser.parse(model_path)

    func = "llik" if llik else "rmse"

    optimizer = Optimizer(mpt, data_path, sep=sep, func=func, ignore_params=ignore, out='../out/eval_inf_g.txt')
    
    optimizer.init_deletion()
    optimizer.random_search()

    # Print the result
    print()



if __name__ == "__main__":

    ARGS = parse_commandlineargs()
    run(**ARGS)