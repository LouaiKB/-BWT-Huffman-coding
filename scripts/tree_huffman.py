# coding ~utf-8
"""

Author: Louai KB

Binary tree classes to implement the Huffman Binary Tree for the compression process.

"""

class TreeNode:

    """This class implements the nodes of the tree"""

    def __init__(self, data : any, character:str=None) -> None:

        """Constructor of our TreeNode class

        Args:
            data (any): data of our tree node
            character(str): the character for the leaf
        """
        self.right_child = None
        self.left_child = None
        self.data = data
        self.character = character

    def __str__(self) -> str:

        """ Prints a string representation of our tree Node
            as the newick format (left child [character] : right child [character])father node

        Returns:
            str: string representation
        """
        if self.right_child is None and self.left_child is None:
            return str(self.data)

        return "(%s [%s]: %s [%s]) : %s" % (str(self.left_child),
                                   self.left_child.character,
                                   str(self.right_child),
                                   self.right_child.character,
                                   str(self.data))

    def is_leaf(self) -> bool:
        """ a method to check whether a node is a leaf or not.
            a leaf has no left child nor right child.

        Returns:
            bool: True if it's leaf False otherwise.
        """
        return self.left_child is None and self.right_child is None    
    
class Tree:

    """This class represents the binary tree"""

    def __init__(self, node : TreeNode) -> None:

        """Constructor of our Tree Class

        Args:
            node (TreeNode): the root node of the tree
        """
        self.node = node
        self.encoder = {}
    
    def number_of_leafs(self, node : TreeNode) -> int:

        """ a recursive method to compute the number of leafs of a binary tree

        Returns:
            [int]: number of leafs
        """

        if node is None:
            return 0

        if node.left_child is None and node.right_child is None:
            return 1
        
        return self.number_of_leafs(node.left_child) + self.number_of_leafs(node.right_child)
