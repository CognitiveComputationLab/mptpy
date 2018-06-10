""" Functions for parsing MPT models in the bmpt format.

Copright 2018 Cognitive Computation Lab
University of Freiburg
Paulina Friemann <friemanp@cs.uni-freiburg.de>
Nicolas Riesterer <riestern@cs.uni-freiburg.de>

"""


class BmptParser():

    def __init__(self):
        self.leaves = []
        self.word = ""
        self.leaf_test = None

    def parse(self, file_path):
        """ Parse the mpt from the file

        Parameters
        ----------
        file_path : str
            path to the model file

        Returns
        -------
        """
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
        self.leaves = self.get_leaf_info(lines) #retrieve leaf information
        self.word = self.get_word(lines) #retrieve the mpt word
        self.leaf_test = self.construct_leaf_test(self.leaves)
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

    def get_leaf_info(self, lines):
        """ If there is information about the leaves in the file,
        retrieve and return it

        Parameters
        ----------
        lines : [str]
            file content without comments

        Returns
        -------
        [str]
            list with leaf names
        """
        leaves = list(filter(lambda x: x[0] == "[", lines))
        if leaves:
            leaves = leaves[0].strip()
            leaves = leaves.replace("[", "").replace("]", "").split(",")
            leaves = [leaf.lstrip() for leaf in leaves]
        return leaves

    def construct_leaf_test(self, leaves):
        """ Constructs the test for leaves

        Parameters
        ----------
        leaves : [str]
            list of leaf names
        
        Returns
        -------
        func
            leaf test
        """
        func = lambda ch : ch in leaves
        return func

    def get_word(self, lines):
        """ Retrieve the mpt from the file content

        Parameters
        ----------
        lines : [str]
            file content without comments

        Returns
        -------
        str
            mpt word
        """
        lines = list(filter(lambda x: x[0] != "[", lines))
        word = lines[0]
        return word

