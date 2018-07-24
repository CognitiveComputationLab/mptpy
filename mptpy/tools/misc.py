""" Miscellaneous helper functions.

| Copyright 2018 Cognitive Computation Lab
| University of Freiburg
| Nicolas Riesterer <riestern@cs.uni-freiburg.de>
| Paulina Friemann <friemanp@cs.uni-freiburg.de>

"""


import os


def merge_dicts(*dicts):
    """ Merge two dictionaries
    example: merge({1:'a', 2:'b'}, {1:'c'}) -> {1:['a','c'], 2:['c']}

    Parameters
    ----------
    dicts
        Dictionaries to be merged
    """
    temp = {}

    for d in (dicts):

        for key, value in d.items():
            if key in temp.keys():
                temp[key].extend(value)
            else:
                temp[key] = value
    return temp


def write_iterable_to_file(path, it, newline=True):
    """ Writes an iterable to a file.
    creates new file if not existent.

    Parameters
    ----------
    path : str
        path to file

    it : iterable
        iterable to write to file

    newline : boolean
        whether a newline should be placed after each element in it
    """

    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'w') as file_:
        for line in it:
            file_.writelines(line)
            if newline:
                file_.write('\n')
