import random

class TreapBase:
    class Node:
        def __init__(self, key, value, priority = 1):
            self._key = key
            self._value = value
            self._left = self._right = None
            self._priority = priority

    # these methods stay the same no matter which Treap we're usuing

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def __delitem__(self, key):  # implements 'del tree[key] '
        self._root = TreapBase._tree_remove(self._root, key)
        # decrease size
        self._size -= 1


    # allows to print the tree in in-order notation (test purpose only)
    def __str__(self):
        return TreapBase.tree_as_string(self._root)

    @staticmethod
    def tree_as_string(node):
        # function for visualising trees created with parse() (testing purpose only)
        if node is None:
            return "- "
        if node._left is None and node._right is None:
            return f"K:{node._key} P:{node._priority} V:{node._value}"
        else:
            out = f"K:{node._key} P:{node._priority} V:{node._value}"
            out += "( "
            out += TreapBase.tree_as_string(node._left)
            out += ", "
            out += TreapBase.tree_as_string(node._right)
            out += " ) "
            return out

    # tree find, insert and remove implementations

    @staticmethod
    def _tree_find(node, key, is_dynamic_treap):  # internal implementation
        # key is not in tree
        if node is None:
            return node, None
        # return value of node if key is found
        if key == node._key:
            if is_dynamic_treap:
                node._priority += 1
            return node, node._value
        # continue search left or right depending on wanted key
        if key < node._key:
            node._left, value = TreapBase._tree_find(node._left, key, is_dynamic_treap)
            if node._left is not None and node._left._priority > node._priority:
                node = TreapBase._tree_rotate_right(node)
            return node, value
        if key > node._key:
            node._right, value = TreapBase._tree_find(node._right, key, is_dynamic_treap)
            if node._right is not None and node._right._priority > node._priority:
                node = TreapBase._tree_rotate_left(node)
            return node, value

    @staticmethod
    def _tree_insert(node, key, value, is_dynamic_treap):  # internal implementation
        # if key is not found create new node with wanted value und key
        if node is None:
            if is_dynamic_treap:
                return TreapBase.Node(key, value), True
            else:
                return TreapBase.Node(key, value, random.randint(0, 32767)), True
        # node with key is found, so change value and return the node to the tree
        if key == node._key:
            node._value = value
            if is_dynamic_treap:
                node._priority += 1
            return node, False
        # countiue search left or right depending on wanted key and switch left and right subtrees accordingly
        if key < node._key:
            node._left, added_node = TreapBase._tree_insert(node._left, key, value, is_dynamic_treap)
            if node._left._priority > node._priority:
                node = TreapBase._tree_rotate_right(node)
        else:
            node._right, added_node = TreapBase._tree_insert(node._right, key, value, is_dynamic_treap)
            if node._right._priority > node._priority:
                node = TreapBase._tree_rotate_left(node)
        return node, added_node

    @staticmethod
    def _tree_remove(node, key):  # internal implementation
        # if key is not found do nothing
        if node is None:
            return None
        # contiue search left or right depending on key
        elif key < node._key:
            node._left = TreapBase._tree_remove(node._left, key)
            if node._left._priority > node._priority:
                node = TreapBase._tree_rotate_right(node)
        elif key > node._key:
            node._right = TreapBase._tree_remove(node._right, key)
            if node._right._priority > node._priority:
                node = TreapBase._tree_rotate_left(node)
        # found key to delete
        else:
            # if no children just delete node
            if node._left is None and node._right is None:
                node = None
            # if only one child just replace to be deleted node with child
            elif node._left is None:
                node = node._right
            elif node._right is None:
                node = node._left
            # if node has two children
            else:
                # predecessor is largest element in left subtree after while-loop
                predecessor = node._left  # find highest key in left subtree
                while predecessor._right is not None:
                    predecessor = predecessor._right
                # change node with predecessor information since all elements in left subtree are smaller and all
                # elements in the right subtree are larger, since predecessor is largest element in left subtree
                node._key = predecessor._key  # set current node to the highest key in the left subtree
                node._value = predecessor._value  # so there is no need to change the right subtree
                # left subtree still has predecessor in it, so remove predecessor (can only have left child or none)
                node._left = TreapBase._tree_remove(node._left, predecessor._key)
        return node

    @staticmethod
    def _tree_rotate_left(node):
        new_root = node._right
        node._right = new_root._left
        new_root._left = node
        return new_root

    @staticmethod
    def _tree_rotate_right(node):
        new_root = node._left
        node._left = new_root._right
        new_root._right = node
        return new_root

    # sort implementation

    @staticmethod
    def _tree_sort(node, array):
        if node is None:
            return
        TreapBase._tree_sort(node._left, array)
        array.append(node._key)
        TreapBase._tree_sort(node._right, array)

    def sort(self):
        # returns sorted array of the tree
        a = []
        TreapBase._tree_sort(self._root, a)
        return a

    # depth implementation

    @staticmethod
    def _depth(node, key):  # internal implementation
        if node is None:
            return 0 # reached sentinel, so no new edges
        # figuring out total depth of the tree
        if key is None:
            left = TreapBase._depth(node._left, key)
            right = TreapBase._depth(node._right, key)
            # return lenght of longest subtree path and add 1 for current node
            return max(left, right) + 1 # return lenght of longest subtree path and add 1 for current node
        if node._key == key:
            return 1
        if node._key > key:
            return TreapBase._depth(node._left, key) + 1
        if node._key < key:
            return TreapBase._depth(node._right, key) + 1


    def depth(self, key=None):
        return TreapBase._depth(self._root, key)

###########################################################################################################

class RandomTreap(TreapBase):
    def __setitem__(self, key, value):  # implements 'tree[key] = value'
        # making sure size only increases if key is not already in the tree
        self._root, added_node = TreapBase._tree_insert(self._root, key, value, False)
        if added_node:
            self._size += 1

    def __getitem__(self, key):  # implements 'value = tree[key]'
        self._root, value = TreapBase._tree_find(self._root, key, False)
        return value

class DynamicTreap(TreapBase):
    def __setitem__(self, key, value):  # implements 'tree[key] = value'
        # making sure size only increases if key is not already in the tree
        self._root, added_node = TreapBase._tree_insert(self._root, key, value, True)
        if added_node:
            self._size += 1

    def __getitem__(self, key):  # implements 'value = tree[key]'
        self._root, value = TreapBase._tree_find(self._root, key, True)
        return value

    @staticmethod
    def _top(node, min_priority, va, root,stopwords):
        if root._priority < min_priority:
            va.sort(reverse=True)
            return va
        elif node._left is not None and min_priority <= node._left._priority:
            DynamicTreap._top(node._left,min_priority, va, root, stopwords)
        elif node._right is not None and min_priority <= node._right._priority:
            DynamicTreap._top(node._right,min_priority, va, root, stopwords)
        else:
            va.append(f"{node._priority}: {node._key}")
            va.sort(key=node._priority)
            node._priority = 1
            DynamicTreap._top(root, min_priority, va, root, stopwords)




    def top(self, min_priority, stopwords):
        va = []
        DynamicTreap._top(self._root, min_priority, va, self._root, stopwords)
        return va



#############################################################################################################


def file_to_textarray(filename):
    s = open(filename, encoding="latin-1").read()
    for k in ',;.:-"\'!?()&#':
        s = s.replace(k, '')
    s = s.lower()
    return s.split()

def textarray_to_treap(text):
    rt = RandomTreap()
    dt = DynamicTreap()
    word_count = 0
    for word in text:
        # die values werden in dieser Übung nicht benötigt, daher zählen wir probehalber die anzahl der wörter
        if rt[word] is None:
            rt[word] = 0
        if dt[word] is None:
            dt[word] = 0

        word_count += 1
        rt[word] += 1
        dt[word] += 1
    return rt, dt, word_count

def compare_trees(tree1, tree2):
    array1 = tree1.sort()
    array2 = tree2.sort()
    if array1 == array2:
        return True
    else:
        return False

def sortInt(array):
    return array[1]


if __name__ == "__main__":
    filenames = ["casanova-erinnerungen-band-2.txt","die-drei-musketiere.txt", "helmholtz-naturwissenschaften.txt"]



    for filename in filenames:
        text = file_to_textarray(filename)
        rt, dt, word_count = textarray_to_treap(text)

        words = file_to_textarray("Stopwords.txt")  # stopwords
        stopwords = set()
        for i in range(len(words) - 1):
            stopwords.add(words[i])

        viparray = dt.top(800,stopwords)    #Relevanz von Wörtern
        for w in range(len(viparray)-1):
            print(f" {viparray[w]} ({w+1})")



        print(f"Der Vergleich der Arrays von {filename} liefert: {compare_trees(rt, dt)}")

        average_depth_random = 0
        average_accesstime_random = 0
        average_depth_dynamic = 0
        average_accesstime_dynamic = 0
        wordlist = []
        for w in text:
            if w not in wordlist:
                d_random = rt.depth(w)
                average_depth_random += d_random
                average_accesstime_random += rt[w] * d_random / len(text)

                d_dynamic = dt.depth(w)
                average_depth_dynamic += d_dynamic
                average_accesstime_dynamic += dt[w] * d_dynamic / len(text)
            else:
                continue
            wordlist += [w]

        average_depth_random = average_depth_random / len(wordlist)-1
        average_depth_dynamic = average_depth_dynamic / len(wordlist)-1

        print(f"""
        {filename}: Es gibt {word_count} Wörter im Text.
        Random Treap hat mittlere Tiefe {average_depth_random} und mittlere Zugriffszeit {average_accesstime_random} ms .
        Dynamic Treap hat mittlere Tiefe {average_depth_dynamic} und mittlere Zugriffszeit {average_accesstime_dynamic} ms .
        """)
        # man sieht, dass zwar bestätigt wird, dass die mittlere Zugriffszeit bei Dynamic besser ist, allerdings wird
        # nicht bestätigt, dass die mittlere Tiefe besser ist.