""" Interface for applying operations to MPTs.

"""


def apply_operations(mpt, operations):
    for operation in operations:
        mpt = operation.apply(mpt)

    return operation

class Operation(object):
    def apply(self):
        pass
