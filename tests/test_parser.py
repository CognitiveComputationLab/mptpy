""" Tests the parsing of MPT models.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""

import os
from nose.tools import assert_equals
from tests.context import mptpy
from mptpy.tools import parsing


MODEL_DIR = os.path.abspath("tests/test_models/test_build")


def test_get_lines():
    """ Test the reading of lines of the file """
    lines = parsing.get_lines(MODEL_DIR + "/test1.model")
    assert_equals(lines, ["a * bc * c", "a * bc * (1-c)", "a * (1-bc) * a + a * (1-bc) * (1-a) * e", "a * (1-bc) * (1-a) * (1-e)", "(1-a) * d", "(1-a) * (1-d)"])


def test_get_only_parameter():
    assert_equals(parsing.get_only_parameter('(1-u)'), 'u')
    assert_equals(parsing.get_only_parameter('u'), 'u')
    assert_equals(parsing.get_only_parameter('u#E5'), 'u')


def test_parsing():
    word = parsing.parse_file(MODEL_DIR + "/test1.model")
    assert_equals(word, "a bc c 0 1 a 2 e 2 3 d 4 5")

    word = parsing.parse_file(MODEL_DIR + "/testBMPT.model")
    assert_equals(word, "a b c 0 1 a 2 e 2 3 def 4 5")
