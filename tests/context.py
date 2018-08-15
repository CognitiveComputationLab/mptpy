import os

from mptpy.tools.parsing import Parser
from mptpy.mpt import MPT


PARSER = Parser()
MPTS = {}

for entry in os.scandir('./tests/test_models/test_build'):
    MPTS[entry.name.split(".")[0]] = PARSER.parse(entry.path)

MPTS["testdeletion"] = MPT("b c 2 1 a 2 d 1 0")
for mpt in MPTS:
    print(mpt, MPTS[mpt])

