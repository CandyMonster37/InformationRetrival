# -*- coding: utf-8 -*-
def _sbst_comparison(v1, v2):
    """ Sorting function by default """
    if v1[0] == v2[0]:
        return 0
    else:
        return -1 if v1[0] < v2[0] else 1


def _sbst_simple_comparison(v1, v2):
    """ Sorting function by default """
    if v1 == v2:
        return 0
    else:
        return -1 if v1 < v2 else 1


class _sbst_node:
    """ Represents tree node """

    def __init__(self, val, parent, direction=None):
        self.level = self.len = 1
        self.left = self.right = None
        self.val = val
        self.is_array = False
        self.parent = parent
        self.direction = direction

    def getval(self):
        return self.val if not self.is_array else self.val[0]

    def addval(self, val):
        if self.is_array:
            self.val.append(val)
        else:
            self.val = [self.val, val]
            self.is_array = True
        self.len += 1


class sbst:
    def __init__(self, comparison_func=_sbst_comparison, source=None):
        """ Constructor. Parameters:
        comparison_func - function (or lambda) that receives 2 parameters
          and returns -1 if first 'less' then second, 1 if 'greater' and
          0 if parameters considered as 'equal'. If not specified, default
          comparison used (in such case stored objects must implement '<'
          and '==' operations).
        source - iterable object. Convenient for immediate initialization."""
        self.root = None
        self.comp_f = comparison_func
        self._len = 0
        if source != None:
            self.addfrom(source)

    def __len__(self):
        return self._len

    def add(self, val):
        """ Inserts value into the tree. """
        self.root = self._insert_into_node(self.root, val, None)

    def addfrom(self, source):
        """ Inserts all values from iterable source. """
        for val in source:
            self.root = self._insert_into_node(self.root, val, None)

    def _skew(self, node):
        if node == None or node.left == None:
            return node
        elif node.left.level == node.level:
            L = node.left
            node.left = L.right
            if L.right:
                L.right.parent = node
                L.right.direction = 'L'
            L.right = node
            L.parent = node.parent
            L.direction = node.direction
            node.parent = L
            node.direction = 'R'
            return L
        else:
            return node

    def _split(self, node):
        if node == None or node.right == None or node.right.right == None:
            return node
        elif node.level == node.right.right.level:
            R = node.right
            node.right = R.left
            if R.left:
                R.left.parent = node
                R.left.direction = 'R'
            R.left = node
            R.parent = node.parent
            R.direction = node.direction
            node.parent = R
            node.direction = 'L'
            R.level += 1
            return R
        else:
            return node

    def _insert_into_node(self, node, val, parent, direction=None):
        if node == None:
            self._len += 1
            return _sbst_node(val, parent, direction)
        else:
            cmp = self.comp_f(val, node.getval())
            if cmp < 0:  # val < node.getval()
                node.left = self._insert_into_node(node.left, val, node, 'L')
            elif cmp > 0:  # val > node.getval()
                node.right = self._insert_into_node(node.right, val, node, 'R')
            else:  # val == node.getval()
                self._len += 1
                node.addval(val)
                return node
            node = self._skew(node)
            node = self._split(node)
            return node

    def forward_from(self, start=None, inclusive=True, \
                     stop=None, stop_incl=False):
        node = self.root
        curr = None
        # cumbersome traversal because tree can be rebalanced during iteration
        while node:
            cmp = -1 if start == None else self.comp_f([start], node.getval())
            if cmp == 0:
                if inclusive:
                    curr = node
                    node = None
                else:
                    node = node.right
            elif cmp < 0:
                curr = node
                node = node.left
            else:
                node = node.right
        while curr:
            if curr.len > 0:
                if stop != None:
                    cmp = self.comp_f(curr.getval(), [stop])
                    if cmp > 0 or cmp == 0 and not stop_incl:
                        return
                if curr.is_array:
                    i = 0  # 'for' is not used because of possible update of curr.val
                    while i < curr.len:
                        yield curr.val[i]
                        i += 1
                else:
                    yield curr.val
            # step forward
            if curr.right:
                curr = curr.right
                while curr.left:
                    curr = curr.left
            else:
                new_curr = curr.parent
                while new_curr and curr.direction == 'R':
                    curr = new_curr
                    new_curr = curr.parent
                curr = new_curr

    def min(self, limit=None, inclusive=True):
        for val in self.forward_from(limit, inclusive):
            return val
        return None

    def nodes_list(self):
        return self._nodes_list(self.root)

    def _nodes_list(self, node):
        if not node:
            return []
        else:
            return self._nodes_list(node.left) + [node] \
                   + self._nodes_list(node.right)


if __name__ == "__main__":
    my_tree = sbst(source=[1, 3, 4, 6, 78, 22])
    print(list(my_tree.forward_from(4)))
