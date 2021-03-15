# coding ~utf-8
"""

Author: Louai KB

Burrows Wheeler Algorithm to transform sequences into Burrows Wheeler Transform
in ordre to reduce entropy and facilitate the Huffman compression process.

"""

class Bwt:

    """Class that implements the transformation of Burrows Weeler"""

    def __init__(self, sequence: str) -> None:

        """Constructor function

        Args:
            sequence (str): the sequence to be transformed by the BWT sequence
        """
        self.sequence = sequence + '$'
        self.bwt_sequence_encryption = None
        self.bwt_sequence_decryption = None

    @staticmethod
    def bwt_construction_matrix(sequence : str) -> None:

        """ static method to create the Burrows Wheeler Matrix that 
            generates the Burrows Wheeler Transform from the original sequence.
            The yielding process is used to create generator in order to
            facilitate the matrix visualization in the view pattern.

        Args:
            sequence (str): the sequence to be transformed by the BWT

        Returns:
           None: the Bwt construction matrix as a generator.
        
        """
        
        yield sequence

        while sequence[-2] != '$':
            sequence = sequence[-1] + sequence[:-1]
            yield sequence

    def bwt_construction(self) -> str:

        """ This method will proceed the construction of the Burrows Wheeler Transform
            using Burrows Wheeler Matrix. 
            Notice: The Burrows Wheeler Transform corresponds to the last column of the 
            BWT Matrix

        Returns:
            str: The Burrows Wheeler Transform (BWT Sequence)
        """

        bwt_construction_matrix = Bwt.bwt_construction_matrix(self.sequence)
        bwt_construction_matrix = sorted(bwt_construction_matrix)
        bwt = ''
        for row in bwt_construction_matrix:
            # we return the last column as a string
            bwt += row[-1]

        return bwt



    @staticmethod
    def bwt_reconstruction_matrix(bwt_sequence : str) -> list:

        """ static method to create the Burrows Wheeler reconstruction matrix 
            that generates the original sequence from the Burrows Wheeler Transform.
            The implementation of the matrix using a list. We will add each character of BWT
            in the list (as a column) than we sort and we will repeat the process until we get 
            the number of columns is equal to the lenght of the BWT.
            
            Notice: The original Sequence is the one which has a '$' in the end. 
        
        Args:
            bwt_sequence (str): the BWT sequence to be retransformed to the original sequence.
        
        Returns:
            list: the Bwt reconstruction matrix
        """

        reconstruction_matrix = list(bwt_sequence)
        reconstruction_matrix.sort()
        
        while len(reconstruction_matrix[0]) != len(bwt_sequence):
            for i in range(0, len(reconstruction_matrix), 1):
                reconstruction_matrix[i] = bwt_sequence[i] + reconstruction_matrix[i]
            reconstruction_matrix.sort()
        
        return reconstruction_matrix


    def yield_(self):
        s = Bwt.bwt_reconstruction_matrix(self.sequence)
        for i in s:
            yield i

    def bwt_reconstruction(self, bwt) -> tuple:

        """ This method will proceed the reconstruction of the sequence
            using the Burrows Wheeler reconstruction matrix.
            we will iterate through each row (sequence) of the matrix once
            we have a sequence that ends with '$' we will break the loop and
            return the sequence.

            the index_row variable is used to store the index of the original sequence
            in the matrix this is useful to color this sequence in the view pattern (GUI)
            when we decrypt the Burrows Wheeler Transform.

        Returns:
            tuple: original sequence and the index of the sequence in the matrix
        """
        bwt_reconstruction_matrix = Bwt.bwt_reconstruction_matrix(bwt)
        for row in bwt_reconstruction_matrix:
            if row[-1] == '$':
                seq = row
                break
        
        index_row = bwt_reconstruction_matrix.index(seq)
        
        return (seq.replace('$', ''), index_row)
