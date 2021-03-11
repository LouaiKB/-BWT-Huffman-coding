# coding ~utf-8
"""

Author: Louai KB

"""
import os.path
from Bio import SeqIO
from huffman_compression import HuffmanCompression
from bwt import Bwt

class Controller:

    """ Controller class """

    def __init__(self, file:str) -> None:

        """[summary]
        """
        self.file = file
        self.sequence = ''
        self.huffman_object = None
        self.bwt_object = None

    def get_sequence_from_file(self) -> None:
        """[summary]

        Args:
            path (str): [description]
        """
        extension = os.path.splitext(self.file)[1]
        
        if extension == '.fasta':
            print('uessss')
            sequence = SeqIO.read(self.file, 'fasta').seq
            self.sequence = sequence

        elif extension == '.txt':
            with open(self.file, 'r') as f:
                line = f.read()
                for character in line:
                    if character != '\n':
                        self.sequence = self.sequence + character
    
    def compression_process_without_bwt(self) -> dict:
        """[summary]

        Returns:
            dict: [description]
        """
        compression_results = {}
        self.huffman_object = HuffmanCompression(self.sequence)
        huffman_tree = self.huffman_object.binary_tree_huffman()
        self.huffman_object.sequence_to_binary_transformation()
        self.huffman_object.binary_to_unicode()

        compression_results['binary_tree_huffman'] = huffman_tree
        compression_results['sequence_to_binary'] = self.huffman_object.sequence_to_binary
        compression_results['binary_to_unicode'] = self.huffman_object.unicode_sequence

        return compression_results
    
    def decompression_process_without_bwt(self) -> dict:
        """[summary]

        Returns:
            dict: [description]
        """
        decompression_results = {}
        self.huffman_object = HuffmanCompression(self.sequence)
        unicode_to_binary = self.huffman_object.unicode_to_binary()
        binary_to_sequence = self.huffman_object.decompression_process()

        decompression_results['unicode_to_binary'] = unicode_to_binary
        decompression_results['binary_to_sequence'] = binary_to_sequence
        return decompression_results

    def bwt_encryption_step_by_step(self) -> tuple:
        """[summary]

        Returns:
            tuple: [description]
        """
        self.bwt_object = Bwt(self.sequence)
        bwt_matrix = self.bwt_object.bwt_construction_matrix(self.bwt_object.sequence)
        bwt_sequence = self.bwt_object.bwt_construction()
        return (bwt_matrix, bwt_sequence)
    
    def bwt_decryption(self) -> tuple:
        """[summary]

        Returns:
            tuple: [description]
        """
        self.bwt_object = Bwt(self.sequence)
        bwt_reconstruction_matrix = self.bwt_object.bwt_reconstruction_matrix(self.sequence)
        bwt_decryption = self.bwt_object.bwt_reconstruction()
        return (bwt_reconstruction_matrix, bwt_decryption)

if __name__ == '__main__':
    obj = Controller("C:\\Users\\Louai KB\\OneDrive - Aix-Marseille Université\\SEMESTRE 2\\Algorithmique et structures des données\\Algorithmique-Project\\NC_009513.fasta")
    obj.get_sequence_from_file()
    print(obj.bwt_decryption()[0])