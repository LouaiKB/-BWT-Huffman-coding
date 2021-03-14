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
        self.bwt_sequence_encryption = None
        self.bwt_sequence_decryption = None

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

    def yield_(self):
        s = Bwt.bwt_reconstruction_matrix(self.sequence)
        for i in s:
            yield i

    def bwt_reconstruction(self, bwt) -> str:
        """ This method will proceed the reconstruction of the sequence

        Returns:
            str: original sequence
        """
        bwt_reconstruction_matrix = Bwt.bwt_reconstruction_matrix(bwt)
        for row in bwt_reconstruction_matrix:
            if row[-1] == '$':
                seq = row
                break
        index_row = bwt_reconstruction_matrix.index(seq)
        return (seq.replace('$', ''), index_row)

if __name__ == '__main__':
    # from Bio import SeqIO
    # seq = SeqIO.read("C:\\Users\\Louai KB\\OneDrive - Aix-Marseille Université\\SEMESTRE 2\\Algorithmique et structures des données\\Algorithmique-Project\\NC_009513.fasta", 'fasta').seq
    x = Bwt('ATCATCACGATCTACG')
    a = x.bwt_construction()
    print(Bwt.bwt_reconstruction_matrix('AC$GCCTAAACAG'))
    print(x.bwt_reconstruction('AC$GCCTAAACAG')[1])
    # for i in Bwt.bwt_reconstruction_matrix('ATCATCGAGCATCAGATGATCGTACGATCTACG$'):
    #     print(i)