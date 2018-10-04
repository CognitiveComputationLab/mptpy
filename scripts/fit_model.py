""" Fit an MPT model and return the calculated metrics.
Usage: python3 -m fit_model <model_file> <data_file>

"""

import argparse

from mptpy.tools.parsing import Parser
import mptpy.fitting.scipy_fit as fitting


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

    args = parser.parse_args()
    return vars(args)

def run(model_path, data_path, sep=',', header=None, n_optim=10, llik=False):
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
    mpt.draw()
    func = "llik" if llik else "rmse"

    evaluation = fitting.fit_mpt(mpt, func, data_path, sep=sep, n_optim=n_optim)

    # Print the result
    print()
    for key, value in evaluation.items():
        print("{}: {}".format(key, value))

if __name__ == "__main__":
    ARGS = parse_commandlineargs()
    run(**ARGS)
