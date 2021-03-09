# coding ~utf-8
"""

Author: Louai KB

"""

class Bwt:

    """Class that implements the transformation of Burrows Weeler"""

    def __init__(self, sequence: str) -> None:

        """Constructor function

        Args:
            sequence (str): the sequence to be transformed by the BWT
        """
        self.sequence = sequence + '$'

    @staticmethod
    def bwt_construction_matrix(sequence : str) -> None:

        """ static method to create the matrix that generates 
            the bwt sequence from the original sequence.

        Args:
            sequence (str): the sequence to be transformed by the BWT

        Returns:
            list: the Bwt construction matrix
        """
        yield sequence

        while sequence[-2] != '$':
            sequence = sequence[-1] + sequence[:-1]
            yield sequence
    
    @staticmethod
    def bwt_reconstruction_matrix(bwt_sequence : str) -> list:
        """ static method to create the matrix that generates the original sequence
            from the bwt sequence.

        Args:
            bwt_sequence (str): the BWT sequence to be retransformed to the original

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
    
    def bwt_construction(self) -> str:

        """ This method will proceed the construction of the bwt sequence

        Returns:
            str: a bwt sequence
        """

        bwt_construction_matrix = Bwt.bwt_construction_matrix(self.sequence)
        bwt_construction_matrix = sorted(bwt_construction_matrix)
        bwt = ''
        for row in bwt_construction_matrix:
            # we return the last column as a string
            bwt += row[-1]
        
        return bwt

    def bwt_reconstruction(self) -> str:
        """ This method will proceed the reconstruction of the sequence

        Returns:
            str: original sequence
        """
        bwt = self.bwt_construction()
        bwt_reconstruction_matrix = Bwt.bwt_reconstruction_matrix(bwt)

        for row in bwt_reconstruction_matrix:
            if row[-1] == '$':
                seq = row
                break

        return seq

if __name__ == '__main__':
    x = Bwt('ACTTGATC')
    print(x.bwt_construction())