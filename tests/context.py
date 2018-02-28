import os
import sys
PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../mptpy'))
print(PATH)

sys.path.insert(0, PATH)

import mptpy

import mptpy.mpt
