""" Functions for parsing MPT models in the easy format.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


class EasyParser():

    def __init__(self):
        pass

    def read(self, file_path):
        pass

    def open(self, file_path):
        """ Opens the file and stores its contents

        Parameters
        ----------
        file_path : str
            path to the mpt file
        """
        mpt_file = open(file_path, 'r')
        lines = self.strip(mpt_file.readlines()) #remove comments
        mpt_file.close()

    def strip(self, lines):
        """ Removes comments, new lines and empty lines from the file content

        Parameters
        ----------
        lines : [str]
            file content

        Returns
        -------
        [str]
            file content without comments
        """
        criteria = lambda line: line[0] != "#" and line != "\n"
        lines = filter(criteria, lines) #commentary and empty lines
        lines = [line.split("#")[0].strip() for line in lines] #in-line
        
        return lines