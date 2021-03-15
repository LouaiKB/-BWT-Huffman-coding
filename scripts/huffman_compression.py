# coding ~utf-8
"""
Author: Louai KB
"""
from tree_huffman import TreeNode
from tree_huffman import Tree
from Bio import SeqIO
from bwt import Bwt

class HuffmanCompression:

    """This class implements the Huffman compression"""

    def __init__(self, sequence : str) -> None:

        """Constructor of our class
        Args:
            sequence (str): the sequence to be compressed, ex: The Burrows Wheeler Transform.
        """
        self.sequence_to_compress = sequence
        self.sequence_to_binary = ''
        self.unicode_sequence = ''
        
    @staticmethod
    def frequency_calculator(sequence : str) -> dict:

        """ this static method allows us to compute the frequency of each
            character in the sequence.
        Args:
            sequence (str): the sequence to be compressed

        Returns:
            dict: the output will be a dictionnary, keys represent the character
            and the values represent the frequence (a dict for character frequencies).
        """
        characters_frequency = dict()

        for character in sequence:
            if not character in characters_frequency:
                characters_frequency[character] = 0

            characters_frequency[character] = characters_frequency[character] + 1

        return characters_frequency

    @staticmethod
    def two_minimum_nodes(list_of_nodes : list) -> tuple:

        """ this static method determines the tow minimum nodes
            it searches for the first minimum, then it delets it
            from the list in order to find the second minimum.

        Args:
            list_of_nodes (list): list of nodes (TreeNode) objects.

        Returns:
            tuple: the first and the second minimums in a tuple
        """

        minimum_node_one = list_of_nodes[0]

        for i in range(1, len(list_of_nodes), 1):
            if minimum_node_one.data >= list_of_nodes[i].data:
                minimum_node_one = list_of_nodes[i]

        list_of_nodes.remove(minimum_node_one)

        minimum_node_two = list_of_nodes[0]

        for i in range(1, len(list_of_nodes), 1):
            if minimum_node_two.data >= list_of_nodes[i].data:
                minimum_node_two = list_of_nodes[i]

        list_of_nodes.remove(minimum_node_two)

        return (minimum_node_one, minimum_node_two)

    def binary_tree_huffman(self) -> Tree:

        """ this method constructs the Huffman binary tree

        Returns:
            Tree: the binary tree
        """
        # creating the dictionnary of the character frequencies.
        characters_frequency = HuffmanCompression.frequency_calculator(self.sequence_to_compress)
        list_of_nodes = []

        # loop through the dictionnary and create TreeNode object for each character
        # by passing the data (value) and the character (key)
        for key in characters_frequency:
            node = TreeNode(characters_frequency[key], key)
            list_of_nodes.append(node)

        root = list_of_nodes[0]
        tree_object = Tree(root)

        while tree_object.number_of_leafs(root) != len(characters_frequency):
            lowest_nodes = HuffmanCompression.two_minimum_nodes(list_of_nodes)
            
            root = TreeNode(lowest_nodes[0].data + lowest_nodes[1].data)
            list_of_nodes.append(root)
            
            root.left_child = lowest_nodes[1]
            root.right_child = lowest_nodes[0]
            
            tree_object.node = root

        return root

    @staticmethod
    def make_code(node : TreeNode, current_code : str, encoder : dict) -> dict:

        """ This static method implements the "depth first search" recursive algorithm to
            create the binary code (path of each character in the tree) resulting
            from traversing the Huffman binary tree and put 
            the binary code as a value for each caracter as a key
            in the encoder dictionnary.

        Args:
            node (TreeNode): the TreeNode object
            current_code (str): current binary code
            encoder(dict): the encoder key = character, value = binary code
        
        Returns:
            encoder(dict): encoder dictionnary.
        """

        if node is None:
            return

        if node.character is not None:
            encoder[node.character] = current_code
        
        # if we go from the parent node to the left child then the path is 1 else is 0.
        
        HuffmanCompression.make_code(node.left_child, current_code + '1', encoder)
        HuffmanCompression.make_code(node.right_child, current_code + '0', encoder)

        return encoder

    @staticmethod
    def code_generator(root : TreeNode) -> dict:

        """ Code generator method, it calls the make_code
            recursive function to generate binary code (path of each
            caracter in the tree).

        Args:
            root (TreeNode): the huffmain tree

        Returns:
            dict: an encoder which has characters in the keys and the
            binary code in the values
        """

        current_code = ''
        binary_code = {}
        encoder = HuffmanCompression.make_code(root, current_code, binary_code)
        return encoder

    def sequence_to_binary_transformation(self) -> None:

        """ This method transforms the sequence into a binary sequence
            usinf the encoder dictionnaru (paths of every character).
        """
        root = self.binary_tree_huffman()
        encoder = HuffmanCompression.code_generator(root)
        for character in self.sequence_to_compress:
            self.sequence_to_binary = self.sequence_to_binary + encoder[character]

    @staticmethod
    def padding_binary(binary : str) -> tuple:

        """ this static method adds 0 to the end of the binary sequence 
            in order to make it divisible by 8 (because the binary sequence will 
            be coded in 8-bits) and counts the number of added
            0 in order to delete them after transforming the encoding caracters to binary
            for the decompression process. 

        Args:
            binary (str): binary sequence

        Returns:
            tuple: (binary sequence with added 0 and the number of added 0)
        """
        added_zeros = 0

        while len(binary) % 8 != 0:
            binary = binary + '0'
            added_zeros = added_zeros + 1

        return (binary, added_zeros)

    def binary_to_unicode(self) -> None:

        """ this method transforms the binary code into unicode characters (Utf-8).
        """
        padding_results = HuffmanCompression.padding_binary(self.sequence_to_binary)
        padded_binary_sequence = padding_results[0]

        for i in range(0, len(padded_binary_sequence), 8):
            binary_code = padded_binary_sequence[i:i+8]
            binary_transformation = int(binary_code, 2)
            self.unicode_sequence = self.unicode_sequence + chr(binary_transformation)

    def unicode_to_binary(self) -> str:

        """ this method transforms the unicode sequence into a binary sequence,
            after it deletes the added 0 by calling the padding_binary()
            static method. 
            this method implements the first step of decompression.
        """
        binary = ""

        for char in self.unicode_sequence:
            ord_char = ord(char)
            binary = binary + format(ord_char, '08b')

        padding_results = HuffmanCompression.padding_binary(self.sequence_to_binary)
        number_of_added_zeros = padding_results[1]

        # Now we remove the paddings
        binary = binary[:-number_of_added_zeros]

        return binary

    def decompression_process(self, binary_code:str, dict_encoder:dict) -> str:

        """ this method is used for the decompression process.
            From the binary code and the dict_encoder which is a 
            dictionnary which have characters as key and binary code
            (paths resulting from the huffman binary tree) as a value.
            This method travers the binary code and append each number
            to code variable if this code presents in the values (paths) of the encode
            then we get the key which represents the character.

        Args:
            binary_code (str): the binary sequence.
            dict_encoder (dict): dictionnary of characters and the path of each character
        
        Returns:
            str: decompressed sequence
        """

        keys = dict_encoder.keys()
        values = dict_encoder.values()
        
        keys_list = list(keys)
        values_list = list(values)

        code = ''
        decompression_result = ''

        for number in binary_code:
            code += number
            if code in values_list:
                index = values_list.index(code)
                decompression_result = decompression_result + keys_list[index]
                code = ''
        
        return decompression_result

