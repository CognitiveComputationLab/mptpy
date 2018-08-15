""" Interface for applying operations to MPTs.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


def apply_operations(mpt, operations):
    for operation in operations:
        mpt = operation.apply(mpt)

    return operation


class Operation(object):

    def apply(self):
        pass
