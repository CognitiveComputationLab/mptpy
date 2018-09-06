""" Interface for the fitting and evaluation of MPTs.

"""

import os

import numpy as np

from mptpy.tools import misc


def read_data(data_path, sep=','):
    """ Read out the data and remove the header

    Returns
    -------
    list
        data without header
    """
    data = np.genfromtxt(data_path, delimiter=sep, dtype='int')
    data = remove_header(data)
    return data


def remove_header(data):
    """ Remove the header from the data

    Returns
    -------
    list
        Data without header
    """
    skip = 0
    for line in data:
        if -1 in line:
            skip += 1
        else:
            break

    return data[skip:]


def _compute_parameter_ratios(mpt, data):
    """ Compute the ratios of the static parameters of an MPT model

    Parameters
    ----------
    mpt : MPT
        MPT to be fitted

    data : list
        Observation Data

    Returns
    -------
    dict
        Dictionary of static parameters and their values
    """
    observations = compute_observations(data, mpt.subtrees)

    ratios = comp_param_ratios(observations)
    return ratios


def compute_observations(data, subtrees):
    subtree_observations = []
    idx = 0
    for subtree in subtrees:
        n_cats = len(subtree)
        subtree_observations.append(data[idx:(idx + n_cats)].sum())
        idx += n_cats

    return np.array(subtree_observations)


def comp_param_ratios(observations, prefix_no=0):
    if len(observations) <= 1:
        return {}

    left, right = misc.split_half(observations)

    param_ratio = np.sum(left) / np.sum(observations)

    result_dict = {"{}{}".format("y", prefix_no): param_ratio}

    left_prefix = prefix_no + int(np.ceil(len(observations) / 2))
    result_dict.update(comp_param_ratios(left, left_prefix))

    result_dict.update(comp_param_ratios(right, prefix_no + 1))

    return result_dict


def _save_parameter_ratios(static_params, temp_dir):
    """ Save the restrictions for the static parameters to a file

    Parameters
    ----------
    temp_dir : str
        directory to the restriction files
    """
    with open(temp_dir + "model.restr", "w") as file_:
        for param, value in static_params.items():
            file_.write("{} = {}\n".format(param, value))


def _clear_temp_dir(path):
    """ Recreate the temporary files and create the dir if not existant

    Parameters
    ----------
    path : str
        Path to the temporary files
    """
    if os.path.exists(path + "model.restr"):
        os.remove(path + "model.restr")
    if not os.path.exists(path):
        os.makedirs(path)
