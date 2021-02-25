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
        self.encoder = {}

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

    def make_code(self, node, current_code):

        if node is None:
            return
        if node.character is not None:
            self.encoder[node.character] = current_code
        
        self.make_code(node.left_child, current_code + '1')
        self.make_code(node.right_child, current_code + '0')

    def code_generator(self):
        current_code = ''
        root = self.binary_tree_huffman()
        self.make_code(root, current_code)

                                                                                                                  
n1 = TreeNode(1)
n2 = TreeNode(0)
n3 = TreeNode(3)
n4 = TreeNode(1)
n5 = TreeNode(0)
sequence = 'N N T N A  C T T N G  N N G  T T N C C T A  T A  C C T'


obj = HuffmanCompression(sequence.replace(' ', ''))

obj.code_generator()
print(obj.encoder)