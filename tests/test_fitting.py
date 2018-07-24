""" Tests the fitting of MPT models with scipy.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
import numpy as np
from nose.tools import assert_equals, assert_true
from tests.context import mptpy
from mptpy.tools.parsing import Parser
from mptpy.fitting import fitter, scipy_fit
from mptpy.mpt import MPT

parser = Parser()

MODEL_DIR = os.path.abspath("tests/test_models/")


def test_remove_header():
    """ Test if the removal of the header works """
    data_file = MODEL_DIR + "/broeder-agg.csv"

    data = np.genfromtxt(data_file, delimiter=',', dtype='int')

    data_wo_header = fitter.remove_header(data)
    assert_true((data_wo_header == data[1:]).all())


def test_comp_parameter_ratios():
    """ Test the computing of ratios of static parameters """
    params = {
        "y0": 0.5,
        "y5": 0.4,
        "y8": 0.5,
        "y6": 0.333333333333,
        "y7": 0.5,
        "y1": 0.4,
        "y4": 0.5,
        "y2": 0.333333333333,
        "y3": 0.5}

    for key, value in params.items():
        params[key] = round(value, 1)

    thtm = parser.parse(MODEL_DIR + "/test_build/2htms.txt")

    data = fitter.read_data(MODEL_DIR + "/broeder.csv")
    ratios = fitter._compute_parameter_ratios(thtm, data)
    for key, value in ratios.items():
        ratios[key] = round(value, 1)

    assert_equals(ratios, params)
