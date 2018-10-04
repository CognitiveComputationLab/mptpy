""" Interface for applying operations to MPTs.

"""


from sympy.combinatorics.partitions import RGS_enum, RGS_unrank

from mptpy.optimization.operations.operation import Operation


class Substitution(Operation):
    """ Parameter deletion operation on MPTs """

    def __init__(self, config):
        self.config = config  # {param: rgs}

    def apply(self, word):
        elements = list(word)
        for param, rgs in self.config.items():
            elements = apply_rgs(param, rgs, elements)
        return word.sep.join(elements)


def apply_rgs(param, rgs, mpt_list):
    rgs_idx = 0
    for i, elem in enumerate(mpt_list):

        if elem == param:
            if rgs[rgs_idx] == 0:
                pass
            else:
                mpt_list[i] += str(rgs[rgs_idx])
            rgs_idx += 1

    return mpt_list


def get_RGS(rank, param_occurences):
    rgs = RGS_unrank(rank, param_occurences)
    return rgs


def generate_all(mpt, ignore=None):
    """ Generate all trees possible with this operation

    Parameters
    ----------
    mpt : MPT
        mpt that is to be modified

    """

    if ignore is None:
        ignore = set()

    for param in set(mpt.categories) - set(ignore):
        num = mpt.parameters.count(param)
        for i in range(RGS_enum(num)):
            rgs = RGS_unrank(i, num)
            # return get_parameterization(rgs, param)    # TODO
