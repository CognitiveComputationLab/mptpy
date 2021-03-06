""" Convert an MPT model in the BMPT format to the easy representation.
Usage: python3 -m to_easy <model_file> <output_file>

"""

import sys

from mptpy.tools.parsing import Parser


def run(model_file, save_file):
    """ Draw an MPT modelto the command line

    Parameters
    ----------
    file : str
        path to the model file

    """

    parser = Parser()
    mpt = parser.parse(model_file)
    mpt.save(save_file)

if __name__ == "__main__":
    print(sys.argv)

    if len(sys.argv) < 3:
        print("Usage: python3 -m to_easy <model_file> <output_file>")
        exit()

    run(sys.argv[1], sys.argv[2])
