import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='mptpy',
      version='0.0.7',
      author='Nicolas Riesterer, Paulina Friemann',
      author_email='riestern@cs.uni-freiburg.de, friemanp@cs.uni-freiburg.de',
      description='Module to represent and use multinomial processing trees',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/CognitiveComputationLab/mptpy.git',
      packages=setuptools.find_packages(),
      classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ),
)
