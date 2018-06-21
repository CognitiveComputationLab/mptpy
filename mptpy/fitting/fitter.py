""" Interface for the fitting and evaluation of MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
from abc import ABCMeta, abstractmethod
import numpy as np
import mptpy.tools.joint_tree as jt


class Fitter(object):
    """ Interface class for a tree fitting module """
    __metaclass__ = ABCMeta

    def __init__(self, data_path, sep=',', header=None):
        self.data_path = data_path
        self.sep = sep
        self.header = header

    @abstractmethod
    def fit_mpt(self, mpt, n_optim, use_fia):
        """ Fit the tree and return all metrics """
        pass

    def read_data(self):
        """ Read out the data and remove the header

        Returns
        -------
        list
            data without header
        """
        data = np.genfromtxt(self.data_path, delimiter=self.sep, dtype='int')
        data = self.remove_header(data)
        return data

    def remove_header(self, data):
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

    def _compute_parameter_ratios(self, mpt, data):
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
        static_params = {}
        return jt.compute_ratios(data, mpt.subtrees)

    def _save_parameter_ratios(self, static_params, temp_dir):
        """ Save the restrictions for the static parameters to a file

        Parameters
        ----------
        temp_dir : str
            directory to the restriction files
        """
        with open(temp_dir + "model.restr", "w") as file_:
            for param, value in static_params.items():
                print(param, value)
                file_.write("{} = {}\n".format(param, value))

    def _clear_temp_dir(self, path):
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
