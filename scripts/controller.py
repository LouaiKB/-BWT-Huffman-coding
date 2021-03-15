# coding ~utf-8
"""

Author: Louai KB

"""
import os.path
from Bio import SeqIO
from huffman_compression import HuffmanCompression
from bwt import Bwt

class Controller:

    """ Controller class, that connects between models (bwt and huffman compression) and view (GUI)"""

    def __init__(self, file:str) -> None:

        """Constructor of the class

        Args:
            file(str): path of the file that contains the sequence (format of the file txt or fasta)
        """
        self.file = file
        self.sequence = ''
        self.huffman_object = None
        self.bwt_object = None

    def get_sequence_from_file(self) -> None:

        """ A controller method to retrieve the sequence from the file
            if the extension of the file is (.fasta) then we 
            will use the Bio.SeqIO class in order to get the sequence
            directly from the fasta file.
        """

        extension = os.path.splitext(self.file)[1]
        
        if extension == '.fasta':
            sequence = SeqIO.read(self.file, 'fasta').seq
            self.sequence = sequence

        elif extension == '.txt':
            with open(self.file, 'r') as f:
                line = f.read()
                for character in line:
                    if character != '\n':
                        self.sequence = self.sequence + character

    def compression_process_without_bwt(self, sequence:str) -> dict:
        """ This controller method implements the compression process without BWT 
            (not a full compression).

        Args:
            sequence (str): sequence to be compressed bu the Huffman encoding algorithm.

        Returns:
            dict: a dictionnary that contains the steps of the compression.
        """
        compression_results = {}
        self.huffman_object = HuffmanCompression(sequence)
        huffman_tree = self.huffman_object.binary_tree_huffman()
        self.huffman_object.sequence_to_binary_transformation()
        self.huffman_object.binary_to_unicode()

        compression_results['encoder'] = HuffmanCompression.code_generator(huffman_tree)
        compression_results['Step1: Huffman binary tree'] = huffman_tree.__str__()
        compression_results['Step2: Sequence to binary transfomation'] = self.huffman_object.sequence_to_binary
        compression_results['Step3: Binary to unicode transformation'] = self.huffman_object.unicode_sequence

        return compression_results
    
    def decompression_process_without_bwt(self, unicode_file:str, encoder:dict, binary_co:str) -> dict:
        
        """ This controller method implements the decompression process without BWT 
            (not a full decompression).

        Args:
            unicode_file (str): the file that contains the encoding sequence for the decompression process.
            encoder(dict): a dictionnary taht contains the paths of each character in the Huffman binary tree.
            binary_co(str): the binary sequence.

        Returns:
            dict:  a dictionnary that contains the steps of the decompression.
        """

        unicode = ''
        with open(unicode_file, 'r', encoding='utf8') as f:
            line = f.read()
            for char in line:
                if char != '\n':
                    unicode += char

        decompression_results = {}

        self.huffman_object = HuffmanCompression(self.sequence)
        self.huffman_object.unicode_sequence = unicode
        self.huffman_object.sequence_to_binary = binary_co
  
        unicode_to_binary = self.huffman_object.unicode_to_binary()
        binary_to_sequence = self.huffman_object.decompression_process(binary_co, encoder)

        decompression_results['Step1: the unicode'] = unicode
        decompression_results['Step2: unicode to binary transformation'] = unicode_to_binary
        decompression_results['Step3: binary to sequence'] = binary_to_sequence

        return decompression_results

    def bwt_encryption_step_by_step(self) -> tuple:
        """ This controller method implements the Burrows Wheeler encryption step by step.

        Returns:
            tuple: the Burrows Wheeler construction matrix as a generator to facilitate implementation in 
            the view (Gui) and the Burrows Wheeler Transform
        """
        self.bwt_object = Bwt(self.sequence)
        bwt_matrix = self.bwt_object.bwt_construction_matrix(self.bwt_object.sequence)
        bwt_sequence = self.bwt_object.bwt_construction()
        return (bwt_matrix, bwt_sequence)
    
    def bwt_decryption(self) -> tuple:
        """This controller method implements the Burrows Wheeler decryption.

        Returns:
            tuple: the Burrows Wheeler reconstruction matrix as a generator to facilitate implementation in 
            the view (Gui) and the Burrows Wheeler Transform decoded to the original sequence.
        """
        self.bwt_object = Bwt('')
        self.bwt_object.sequence = self.sequence
        bwt_reconstruction_matrix = self.bwt_object.yield_()
        bwt_decryption = self.bwt_object.bwt_reconstruction(self.sequence)
        return (bwt_reconstruction_matrix, bwt_decryption)
    
