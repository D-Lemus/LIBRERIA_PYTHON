from enum import Enum
from typing_extensions import Self
from typing import TypeVar

T = TypeVar("T")


class Color(Enum):
    RED = 0
    BLACK = 1


class Node:
    def __init__(
        self, key: T, color: Color = Color.RED, parent=None, left=None, right=None
    ) -> None:
        self.parent: Node = parent
        self.left: Node = left
        self.right: Node = right
        self.key: T = key
        self.color: Color = color

    # DFS
    def __repr__(self, nil: Self, level=0):
        # Define the indentation for each level
        indent = "    " * level
        repr_str = f"{indent}Node(k={self.key}, c={self.color}, bh={self.bh(nil)})"
        # Recursively traverse the left and right subtrees
        if self.left != nil:
            repr_str += f"\n{self.left.__repr__(nil, level + 1)}"
        if self.right != nil:
            repr_str += f"\n{self.right.__repr__(nil, level + 1)}"
        return repr_str

    def bh(self, nil: Self) -> int:  # black height
        if self == nil:
            return 1
        bh = max(self.left.bh(nil), self.right.bh(nil)) + (
            1 if self.color == Color.BLACK else 0
        )
        return bh


class RBT:  # (Red Black Tree)
    def __init__(self) -> None:
        self.nil = Node(None, Color.BLACK)  # hojas nulas
        self.root = self.nil

    def __repr__(self) -> str:
        if self.root == self.nil:
            return str(None)
        return self.root.__repr__(self.nil, level=0)

    def assert_bst_property(self) -> bool:
        if self.root == self.nil:
            return True
        return self.__assert_bst_property(self.root)

    def __assert_bst_property(self, x: Node) -> bool:
        if x.left != self.nil and x.right != self.nil:
            return (
                x.left.key <= x.key
                and x.right.key >= x.key
                and self.__assert_bst_property(x.left)
                and self.__assert_bst_property(x.right)
            )
        if x.left != self.nil:
            return x.left.key <= x.key and self.__assert_bst_property(x.left)
        if x.right != self.nil:
            return x.right.key >= x.key and self.__assert_bst_property(x.right)
        return True

    def assert_rbt_property(self) -> bool:
        if self.root == self.nil:
            return True
        return self.root.color == Color.BLACK and self.__assert_rbt_property(self.root)

    def __assert_rbt_property(self, x: Node) -> bool:
        if x == self.nil:
            return x.color == Color.BLACK
        c1 = (
            x.left.color == Color.BLACK and x.right.color == Color.BLACK
            if x.color == Color.RED
            else True
        )  # propiedad roja
        c2 = x.left.bh(self.nil) == x.right.bh(self.nil)  # propiedad negra
        return (
            c1
            and c2
            and self.__assert_rbt_property(x.left)
            and self.__assert_rbt_property(x.right)
        )

    def in_order_walk(self) -> list[T]:
        return self.__in_order_walk(self.root)

    def __in_order_walk(self, x: Node) -> list[T]:
        if x != self.nil:
            return (
                self.__in_order_walk(x.left) + [x.key] + self.__in_order_walk(x.right)
            )
        return []

    def search(self, k: T) -> bool:
        return self.__search(self.root, k) != self.nil

    def __search(self, x: Node, k: T) -> Node:
        while x != self.nil and k != x.key:
            x = x.left if k < x.key else x.right
        return x

    def minimum(self) -> T:
        return self.__minimum(self.root).key

    def __minimum(self, x: Node) -> Node:
        while x.left != self.nil:
            x = x.left
        return x

    def maximum(self) -> T:
        return self.__maximum(self.root).key

    def __maximum(self, x: Node) -> Node:
        while x.right != self.nil:
            x = x.right
        return x

    def successor(self, k: T) -> T:
        x = self.__search(self.root, k)
        if x == self.nil:
            raise ValueError("Key not found")
        s = self.__successor(x)
        return s.key if s != self.nil else None

    def __successor(self, x: Node) -> Node:
        if x.right != self.nil:
            return self.__minimum(x.right)
        y = x.parent
        while y != self.nil and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, k: T) -> T:
        x = self.__search(self.root, k)
        if x == self.nil:
            raise ValueError("Key not found")
        p = self.__predecessor(x)
        return p.key if p != self.nil else None

    def __predecessor(self, x: Node) -> Node:
        if x.left != self.nil:
            return self.__maximum(x.left)
        y = x.parent
        while y != self.nil and x == y.left:
            x = y
            y = y.parent
        return y

    def insert(self, k: T) -> bool:
        if self.search(k):
            return False
        self.__insert(Node(k, Color.RED))
        return True

    def __insert(self, z: Node) -> None:
        # Standard BST insert
        y = self.nil
        x = self.root
        
        # Find the position to insert the new node
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
                
        # Set the parent of z
        z.parent = y
        
        # If the tree was empty, z becomes the root
        if y == self.nil:
            self.root = z
        # Otherwise, set z as a child of y
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z
            
        # Initialize z's children as NIL
        z.left = self.nil
        z.right = self.nil
        
        # Color z red (already set in constructor)
        
        # Fix the RB tree properties that might have been violated
        self.__insert_fixup(z)

    def __insert_fixup(self, z: Node):
        while z.parent.color == Color.RED:
            if z.parent == z.parent.parent.left:  # z's parent is a left child
                y = z.parent.parent.right  # y is z's uncle
                
                # Case 1: z's uncle is red
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    # Case 2: z's uncle is black and z is a right child
                    if z == z.parent.right:
                        z = z.parent
                        self.__left_rotate(z)
                    # Case 3: z's uncle is black and z is a left child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.__right_rotate(z.parent.parent)
            else:  # z's parent is a right child
                y = z.parent.parent.left  # y is z's uncle
                
                # Case 1: z's uncle is red
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    # Case 2: z's uncle is black and z is a left child
                    if z == z.parent.left:
                        z = z.parent
                        self.__right_rotate(z)
                    # Case 3: z's uncle is black and z is a right child
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.__left_rotate(z.parent.parent)
        self.root.color = Color.BLACK

    def delete(self, k: T) -> bool:
        z = self.__search(self.root, k)
        if z != self.nil:
            self.__delete(z)
            return True
        return False

    def __delete(self, z: Node) -> None:
        y = z
        y_original_color = y.color
        
        if z.left == self.nil:  # sin hijos o un hijo derecho
            x = z.right
            self.__transplant(z, z.right)
        elif z.right == self.nil:  # un hijo izquierdo
            x = z.left
            self.__transplant(z, z.left)
        else:  # dos hijos
            y = self.__minimum(z.right)  # successor of z
            y_original_color = y.color
            x = y.right
            
            if y.parent == z:  # y is a direct child of z
                x.parent = y  # in case x is NIL
            else:
                self.__transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
                
            self.__transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
            
        if y_original_color == Color.BLACK:
            self.__delete_fixup(x)
        del z

    def __delete_fixup(self, x: Node):
        while x != self.root and x.color == Color.BLACK:
            if x == x.parent.left:
                w = x.parent.right
                
                if w.color == Color.RED:
                    # Case 1: x's sibling w is red
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.__left_rotate(x.parent)
                    w = x.parent.right
                    
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    # Case 2: w's both children are black
                    w.color = Color.RED
                    x = x.parent
                else:
                    # Case 3: w's right child is black
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.__right_rotate(w)
                        w = x.parent.right
                    
                    # Case 4: w's right child is red
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.__left_rotate(x.parent)
                    x = self.root  # to terminate the loop
            else:
                w = x.parent.left
                
                if w.color == Color.RED:
                    # Case 1: x's sibling w is red
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.__right_rotate(x.parent)
                    w = x.parent.left
                    
                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    # Case 2: w's both children are black
                    w.color = Color.RED
                    x = x.parent
                else:
                    # Case 3: w's left child is black
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.__left_rotate(w)
                        w = x.parent.left
                    
                    # Case 4: w's left child is red
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.__right_rotate(x.parent)
                    x = self.root  # to terminate the loop
                    
        x.color = Color.BLACK

    def __transplant(self, u: Node, v: Node) -> None:
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def __left_rotate(self, x: Node) -> Node:
        if x.right == self.nil:
            raise Exception("Cannot left rotate")
            
        y = x.right
        
        # Turn y's left subtree into x's right subtree
        x.right = y.left
        if y.left != self.nil:
            y.left.parent = x
            
        # Link x's parent to y
        y.parent = x.parent
        if x.parent == self.nil:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        # Put x on y's left
        y.left = x
        x.parent = y
        
        return y

    def __right_rotate(self, y: Node) -> Node:
        if y.left == self.nil:
            raise Exception("Cannot right rotate")
            
        x = y.left
        
        # Turn x's right subtree into y's left subtree
        y.left = x.right
        if x.right != self.nil:
            x.right.parent = y
            
        # Link y's parent to x
        x.parent = y.parent
        if y.parent == self.nil:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
            
        # Put y on x's right
        x.right = y
        y.parent = x
        
        return x


if __name__ == "__main__":

    t = RBT()
    for i in [9, 5, 1, 0, 6, 3, 2, 4, 7, 8]:
        t.insert(i)
    print(t)
    # Node(k=5, c=Color.BLACK, bh=3)
    #     Node(k=1, c=Color.RED, bh=2)
    #         Node(k=0, c=Color.BLACK, bh=2)
    #         Node(k=3, c=Color.BLACK, bh=2)
    #             Node(k=2, c=Color.RED, bh=1)
    #             Node(k=4, c=Color.RED, bh=1)
    #     Node(k=7, c=Color.RED, bh=2)
    #         Node(k=6, c=Color.BLACK, bh=2)
    #         Node(k=9, c=Color.BLACK, bh=2)
    #             Node(k=8, c=Color.RED, bh=1)
    print(t.in_order_walk())
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(t.assert_bst_property())
    # True
    print(t.search(10), t.search(9))
    # False, True
    print(t.minimum(), t.maximum())
    # 0, 9
    print(t.predecessor(5), t.successor(5))
    # 4, 6
    print(t.insert(10), t.assert_bst_property())
    # True, True
    print(t)
    # Node(k=5, c=Color.BLACK, bh=3)
    #     Node(k=1, c=Color.RED, bh=2)
    #         Node(k=0, c=Color.BLACK, bh=2)
    #         Node(k=3, c=Color.BLACK, bh=2)
    #             Node(k=2, c=Color.RED, bh=1)
    #             Node(k=4, c=Color.RED, bh=1)
    #     Node(k=7, c=Color.RED, bh=2)
    #         Node(k=6, c=Color.BLACK, bh=2)
    #         Node(k=9, c=Color.BLACK, bh=2)
    #             Node(k=8, c=Color.RED, bh=1)
    #             Node(k=10, c=Color.RED, bh=1)
    print(t.delete(5), t.assert_bst_property())
    # True, True
    print(t)
    # Node(k=6, c=Color.BLACK, bh=3)
    #     Node(k=1, c=Color.RED, bh=2)
    #         Node(k=0, c=Color.BLACK, bh=2)
    #         Node(k=3, c=Color.BLACK, bh=2)
    #             Node(k=2, c=Color.RED, bh=1)
    #             Node(k=4, c=Color.RED, bh=1)
    #     Node(k=9, c=Color.RED, bh=2)
    #         Node(k=7, c=Color.BLACK, bh=2)
    #             Node(k=8, c=Color.RED, bh=1)
    #         Node(k=10, c=Color.BLACK, bh=2)