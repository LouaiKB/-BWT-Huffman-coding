# coding ~utf-8
"""
Author: Louai KB
"""
from tree_huffman import TreeNode
from tree_huffman import Tree

class HuffmanCompression:

    """This class implements the Huffman compression"""

    def __init__(self, sequence : str) -> None:

        """Constructor of our class
        Args:
            sequence (str): the sequence to be compressed
        """
        self.sequence_to_compress = sequence
        self.sequence_to_binary = ''
        self.unicode_sequence = ''
        
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
        characters_frequency = dict()

        for character in sequence:
            if not character in characters_frequency:
                characters_frequency[character] = 0

            characters_frequency[character] += 1

        # copy() to avoid runtime error
        for key in characters_frequency.copy():
            if characters_frequency[key] == 0:
                characters_frequency.pop(key)

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

        """ this method constructs the binary tree

        Returns:
            Tree: the binary tree
        """
        characters_frequency = HuffmanCompression.frequency_calculator(self.sequence_to_compress)
        list_of_nodes = []

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
    def make_code(node : TreeNode, current_code : str, encoder : dict) -> None:

        """ This recursive method creates binary code
            from traversing the binary tree and put 
            the binary code for each caracter 
            in the encoder attribute.
        Args:
            node (TreeNode): the TreeNode object
            current_code (str): current binary code
        """

        if node is None:
            return

        if node.character is not None:
            encoder[node.character] = current_code
        
        HuffmanCompression.make_code(node.left_child, current_code + '1', encoder)
        HuffmanCompression.make_code(node.right_child, current_code + '0', encoder)

        return encoder

    @staticmethod
    def code_generator(root : TreeNode) -> dict:

        """ Code generator method, it calls the make_code
            recursive function to generate binary code.

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

        """ This method transform the sequence into binary code
        """
        root = self.binary_tree_huffman()
        encoder = HuffmanCompression.code_generator(root)
        for character in self.sequence_to_compress:
            self.sequence_to_binary += encoder[character]

    @staticmethod
    def padding_binary(binary : str) -> tuple:

        """ this static method adds 0 to the end of the binary sequence 
            in order to make it divisible by 8 and counts the number of added
            0 in order to delete them after transforming the caracters to binary. 

        Args:
            binary (str): binary sequence

        Returns:
            tuple: (binary sequence with added 0 and the number of added 0)
        """
        added_zeros = 0

        while len(binary) % 8 != 0:
            binary += '0'
            added_zeros += 1

        return (binary, added_zeros)

    def binary_to_unicode(self) -> None:

        """ this method transforms the binary code into unicode characters,
            after that it will create a compressed sequence file in order to
            store the unicode characters code in this file.
            this file contains the compressed sequence
        """
        padding_results = HuffmanCompression.padding_binary(self.sequence_to_binary)
        padded_binary_sequence = padding_results[0]

        for i in range(0, len(padded_binary_sequence), 8):
            binary_code = padded_binary_sequence[i:i+8]
            binary_transformation = int(binary_code, 2)
            self.unicode_sequence += chr(binary_transformation)

        with open('compressed_sequence.txt', 'wb') as file:
            encode = self.unicode_sequence.encode('utf-8')
            file.write(encode)

    def unicode_to_binary(self) -> str:

        """ this method transforms the unicode characters into binary,
            after it deletes the added 0 by calling the padding_binary()
            static method. 
            this method implements the first step of decompression.
        """
        binary = ""

        for char in self.unicode_sequence:
            ord_char = ord(char)
            binary += '{:08b}'.format(ord_char)

        padding_results = HuffmanCompression.padding_binary(self.sequence_to_binary)
        number_of_added_zeros = padding_results[1]
        binary = binary[:-number_of_added_zeros]

        return binary




if __name__ == '__main__':

    sequence = 'ACTGC'

    obj = HuffmanCompression(sequence.replace(' ', ''))
    obj.sequence_to_binary_transformation()
    print(obj.sequence_to_binary)
    obj.binary_to_unicode()
    print(obj.unicode_to_binary())
