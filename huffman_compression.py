# coding ~utf-8
"""

Author: Louai KB

"""
from tree_huffman import Node

class HuffmanCompression:

    """This class implements the Huffman compression"""

    def __init__(self, sequence : str) -> None:

        """Constructor of our class

        Args:
            sequence (str): the sequence to be compressed
        """
        self.sequence_to_compress = sequence

    @staticmethod
    def frequency_calculator(sequence : str) -> dict:

        """ this static method allows to compute the frequency of each
            character in the sequence

        Args:
            sequence (str): the sequence to be compressed

        Returns:
            dict: the output will be a dictionnary, keys represent the character
            and the values represent the frequence.
        """
        characters_frequency = dict([
                                    ('A', 0),
                                    ('C', 0),
                                    ('G', 0),
                                    ('T', 0),
                                    ('N', 0)])
        for charcater in sequence:

            if charcater == 'A':
                characters_frequency['A'] += 1

            elif charcater == 'C':
                characters_frequency['C'] += 1

            elif charcater == 'G':
                characters_frequency['G'] += 1

            elif charcater == 'T':
                characters_frequency['T'] += 1

            elif charcater == 'N':
                characters_frequency['N'] += 1

        return characters_frequency

    def binary_tree_huffman(self):
        pass 

