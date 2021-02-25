# coding ~utf-8
"""

Author: Louai KB

"""

class TreeNode:

    """This class implements the nodes of the tree"""

    def __init__(self, data : any, character=None) -> None:

        """Constructor of our TreeNode class

        Args:
            data (any): data of our tree node
        """
        self.right_child = None
        self.left_child = None
        self.data = data
        self.character = character

    def __str__(self) -> str:

        """ Prints a string representation of our tree Node
            as a nawick-like format
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

    def is_leaf(self):
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

        if node is None:
            return 0

        if node.left_child is None and node.right_child is None:
            return 1
        
        return self.number_of_leafs(node.left_child) + self.number_of_leafs(node.right_child)































        
        # if root is None:
        #     raise Exception('Node is empty')

        # queue = [root]
        # encoder = {}
        # binary_code = ''
        # father_node = root
        # grand_father_node = root

        # while len(queue) > 0:
        #     if len(queue) == 1:
        #         father_node = grand_father_node
        #         binary_code = binary_code[:-1]

        #     node = queue.pop()
        #     if node == father_node.left_child:
        #         binary_code += '1'

        #     elif node == father_node.right_child:
        #         binary_code += '0'

        #     if node.right_child is not None:
        #         queue.append(node.right_child)


        #     if node.left_child is not None:
        #         queue.append(node.left_child)
            
        #     elif node.is_leaf():
        #         encoder[node.character] = binary_code
        #         binary_code = binary_code[:-1]

        #     if not node.is_leaf():
        #         grand_father_node = father_node
        #         father_node = node

        # return encoder
        
        
        

