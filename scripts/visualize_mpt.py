""" Draw an MPT model to the command line.
Usage: python3 -m visualize_mpt <model_file>

"""


import sys

from mptpy.tools.parsing import Parser


def run(file):
    """ Draw an MPT modelto the command line

    Parameters
    ----------
    file : str
        path to the model file

    """

    parser = Parser()
    mpt = parser.parse(file)
    mpt.draw()
    print(mpt)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 -m visualize_mpt <model_file>")
        exit()

    run(sys.argv[1])
