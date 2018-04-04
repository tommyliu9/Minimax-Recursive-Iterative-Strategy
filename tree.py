"""
Represents a Treee
Pulled the Tree Class from:
http://www.cdf.utoronto.ca/~csc148h/winter/lecturedata/AbdulAziz/W7/trees_api_fri.py
"""
from typing import List

class Tree:
    """
    A Modified Tree ADT that identifies the root with the entire tree.
    """
    def __init__(self, value: object = None, score: int = None,\
                 p1_turn: bool = None, children: List['Tree'] = None) -> None:
        """
        Create Tree self with content value and 0 or more children
        """
        self.value = value
        # copy children if not None
        self.score = score
        self.is_p1_turn = p1_turn
        self.children = children.copy() if children else []

    def __str__(self, indent=0):
        """
        Produce a user-friendly string representation of Tree self,
        indenting each level as a visual clue.

        @param Tree self: this tree
        @param int indent: amount to indent each level of tree
        @rtype: str

        >>> t = Tree(17)
        >>> print(t)
        17 None
        """
        root_str = indent * " " + str(self.value) + " " + str(self.score)
        mid = len(self.non_none_kids()) // 2
        left_str = [c.__str__(indent + 3)
                    for c in self.non_none_kids()][: mid]
        right_str = [c.__str__(indent + 3)
                     for c in self.non_none_kids()][mid:]
        return '\n'.join(right_str + [root_str] + left_str)

    def non_none_kids(self):
        """ Return a list of Tree self's non-None children.

        @param Tree self:
        @rtype: list[Tree]
        """
        return [c
                for c in self.children
                if c is not None]

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")