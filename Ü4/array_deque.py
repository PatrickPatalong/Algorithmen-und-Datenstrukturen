import doctest
import pytest



class array_deque:

    def __init__(self):                   # constructor for empty container
        '''your documentation here'''
        self.size_ = 0                    # no item has been inserted yet
        self.capacity_ = 1                # we reserve memory for at least one item
        self.data_ = [None]               # internal memory (init one free cell)
        ...                               # your code here
        
    def size(self):
        '''your documentation here'''
        return self.size_
        
    def capacity(self):
        '''your documentation here'''
        return self.capacity_                      # your code here
        
    def push(self, item):                 # add item at the end
        '''your documentation here'''
        if self.capacity_ == self.size_:  # internal memory is full
            doublememoryarray = array_deque()
            doublememoryarray.size_ = self.size_
            doublememoryarray = list(self)         # your code to double the memory

            self = doublememoryarray.copy
            array_deque.push(self,item)

        self.size_ += 1
        ...                               # your code to insert the new item
        
    def pop_first(self):
        '''your documentation here'''
        if self.size_ == 0:
            raise RuntimeError("pop_first() on empty container")
        ...                               # your code here
        
    def pop_last(self):
        '''your documentation here'''
        if self.size_ == 0:
            raise RuntimeError("pop_last() on empty container")
        ...                               # your code here
        
    def __getitem__(self, index):         # __getitem__ implements v = c[index]
        '''your documentation here'''
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        return ...                        # your code here
        
    def __setitem__(self, index, v):      # __setitem__ implements c[index] = v
        '''your documentation here'''
        if index < 0 or index >= self.size_:
            raise RuntimeError("index out of range")
        ...                               # your code here
        
    def first(self):
        '''your documentation here'''
        return ...                        # your code here
        
    def last(self):
        '''your documentation here'''
        return ...                        # your code here
        
    def __eq__(self, other):
        '''returns True if self and other have same size and elements'''
        ...                               # your code here

    def __ne__(self, other):
        '''returns True if self and other have different size or elements'''
        return not (self == other)

###########################################################

class slow_array_deque(array_deque):

    def push(self, item):                 # add item at the end
        if self.capacity_ == self.size_:  # internal memory is full
            ...                           # code to enlarge the memory by one
        self.size_ += 1
        ...                               # your code to insert the new item

###########################################################

def test_array_deque():
    ...                                   # your tests here
