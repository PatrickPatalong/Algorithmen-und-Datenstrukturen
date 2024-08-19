from random import randint

import pytest


class Student:
    def __init__(self, name, mark):
        """
        Construct new Student object with given 'name' and 'mark'.

        :param name: name of the student
        :param mark: mark of the student
        """
        self._name = name
        self._mark = mark

    def get_name(self):
        """
        Access the name.
        :return: Returns the name of the student.
        """
        return self._name

    def get_mark(self):
        """
        Access the mark.
        :return: Returns the mark of the student.
        """
        return self._mark

    def __repr__(self):
        """
        Convert Student object to its string representation.
        :return:
        """
        return "%s: %3.1f" % (self._name, self._mark)

    def __eq__(self, other):
        """
        Check if two Student objects are equal.
        :param other: some other object
        :return: Returns True if both objects have the same attributes otherwise False.
        """
        return self._name == other._name and self._mark == other._mark


##################################################################

def insertion_sort_1(a, key=lambda x: x):
    '''
    Sort the array 'a' in-place.

    Parameter 'key' must hold a function that, given a complicated
    object, extracts the property to sort by. By default, this
    is the object itself (useful to sort integers). To sort Students
    by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.
    
    NOTE: THIS IMPLEMENTATION INTENTIONALLY CONTAINS A BUG, 
    WHICH YOUR TESTS ARE SUPPOSED TO DETECT.
    
    The bug is: current is shifted to the left until a[j-1] is smaller.
    That is, it will be shifted to the left of elements that are equal.
    This contradicts the requirement that the order of equal elements
    must remain stable.
    '''
    for i in range(1, len(a)):
        current = a[i]
        j = i
        while j > 0:
            if key(a[j-1]) < key(current):
                break
            else:
                a[j] = a[j-1]
            j -= 1
        a[j] = current

##################################################################

def insertion_sort(a, key=lambda x: x):
    """
    Sort the array 'a' in-place.
    To sort Students by name, you call:
        insertion_sort_1(students, key=Student.get_name)
    whereas to sort by mark, you use
        insertion_sort_1(students, key=Student.get_mark)
    This corresponds to the behavior of Python's built-in sorting functions.

    :param key: Parameter 'key' must hold a function that, given a complicated object, extracts the property to sort
    by. By default, this is the object itself (useful to sort integers).
    """
    for i in range(1, len(a)):
        current = a[i]
        k = i
        while k > 0:
            # the bodies of the if and else case were swapped in insertion_sort_1
            if key(current) < key(a[k - 1]):
                a[k] = a[k - 1]
            else:
                break
            k -= 1
        a[k] = current


##################################################################

def selection_sort(a, key=lambda x: x):
    """
    Sort the array 'a' in-place.
    """
    array_size = len(a)
    for i in range(array_size - 1):
        m = i
        for k in range(i + 1, array_size):
            if key(a[k]) < key(a[m]):
                m = k
        a[i], a[m] = a[m], a[i]


##################################################################

def merge_sort(a, key=lambda x: x):
    array_size = len(a)
    if array_size <= 1:
        return a

    left = merge_sort(a[:array_size // 2], key)
    right = merge_sort(a[array_size // 2:], key)

    res = []
    i, j = 0, 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    return res + left[i:] + right[j:]


###################################################################

@pytest.fixture
def arrays():
    """
    Create a dictionary holding test data. 
    
    This function is annotated as 'pytest.fixture'.
    This instructs 'pytest' to call this function before every 
    "test_" function that contains the name 'arrays' as a parameter.
    The fixture function creates test data that is passed to the test
    function in this parameter.
    This has two important advantages:
    * Each test function using the fixture starts in a well-defined 
      initial state.
    * A redundant implementation of identical test data creation 
      is avoided.

    :return: Returns test data.
    """

    data = dict()

    # integer arrays
    data['int_arrays'] = [
        [],  # empty array
        [1],  # one element
        [2, 1],  # two elements
        [3, 2, 3, 1],  # the array from the exercise text
        [randint(0, 4) for k in range(10)],  # 10 random ints
        [randint(0, 4) for k in range(10)]  # another 10 random ints
    ]

    # Student arrays
    data['student_arrays'] = [
        [Student('Adam', 1.3),
         Student('Bert', 2.0),
         Student('Elsa', 1.0),
         Student('Greg', 1.7),
         Student('Jill', 2.7),
         Student('Judy', 3.0),
         Student('Mike', 2.3),
         Student('Patt', 5.0)],  # without replicated marks

        [Student('Adam', 1.3),
         Student('Bert', 2.0),
         Student('Elsa', 1.3),
         Student('Greg', 1.0),
         Student('Jill', 1.7),
         Student('Judy', 1.0),
         Student('Mike', 2.3),
         Student('Patt', 1.3)],  # with replicated marks, alphabetic

        [Student('Bert', 2.0),
         Student('Mike', 2.3),
         Student('Elsa', 1.3),
         Student('Judy', 1.0),
         Student('Patt', 2.0),
         Student('Greg', 1.0),
         Student('Jill', 1.7),
         Student('Adam', 1.3)]  # with replicated marks, random order
    ]

    return data


def test_builtin_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        a = list(original)
        a.sort()
        check_integer_sorting(original, a)

    # test the Student arrays
    for original in arrays['student_arrays']:
        a = list(original)
        a.sort(key=Student.get_name)
        check_student_sorting(original, a, Student.get_name)

        a = list(original)
        a.sort(key=Student.get_mark)
        check_student_sorting(original, a, Student.get_mark)

        a = list(original)
        a.sort(key=Student.get_name)
        a.sort(key=Student.get_mark)
        check_nested_sorting(original, a)


def test_insertion_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        a = list(original)
        insertion_sort(a)
        check_integer_sorting(original, a)

    # test the Student arrays: sort by mark
    for original in arrays['student_arrays']:
        a = list(original)
        insertion_sort(a, key=Student.get_name)
        check_student_sorting(original, a, Student.get_name)

        a = list(original)
        insertion_sort(a, key=Student.get_mark)
        check_student_sorting(original, a, Student.get_mark)

        a = list(original)
        insertion_sort(a, key=Student.get_name)
        insertion_sort(a, key=Student.get_mark)
        check_nested_sorting(original, a)


def test_selection_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        a = list(original)
        selection_sort(a)
        check_integer_sorting(original, a)

    # test the Student arrays: sort by mark
    for original in arrays['student_arrays'][1:]:
        a = list(original)
        selection_sort(a, key=Student.get_name)
        selection_sort(a, key=Student.get_mark)
        with pytest.raises(AssertionError):
            check_nested_sorting(original, a)


def test_merge_sort(arrays):
    # test the integer arrays
    for original in arrays['int_arrays']:
        a = merge_sort(original)
        check_integer_sorting(original, a)

    # test the Student arrays: sort by mark
    for original in arrays['student_arrays']:
        a = merge_sort(original, key=Student.get_name)
        check_student_sorting(original, a, Student.get_name)

        a = merge_sort(original, key=Student.get_mark)
        check_student_sorting(original, a, Student.get_mark)

        by_name = merge_sort(original, key=Student.get_name)
        by_mark = merge_sort(by_name, key=Student.get_mark)
        check_nested_sorting(original, by_mark)


def test_hierarchical_sort(arrays):
    for original in arrays['student_arrays']:
        intermediate_result = merge_sort(original, key=Student.get_name)
        result = merge_sort(intermediate_result, key=Student.get_mark)

        # test explicitly the stability of the names after sorting by mark
        check_nested_sorting(original, result)

def test_checks():
    # alternative solution
    with pytest.raises(AssertionError):
        check_integer_sorting([1], [])

    with pytest.raises(AssertionError):
        check_integer_sorting([], [1])

    with pytest.raises(ValueError):
        check_integer_sorting([3, 2, 3, 1], [1, 1, 2, 3])

    with pytest.raises(AssertionError):
        check_integer_sorting([3, 2, 3, 1], [3, 2, 3, 1])


def check_integer_sorting(original, result):
    """
    This function has the prefix check_, because it should not be detected as test by the pytest framework
    and instead is called within the test_ functions, which get automatically detected. The check_ prefix
    indicates, that this function does the the real checks, whereas the test functions only contain the test logic.

    :param original: contains the array before sorting
    :param result: contains the output of the sorting algorithm
    :return:
    """
    # both arrays should have same length
    assert len(original) == len(result)

    # all values of original array should still exist
    result_copy = list(result)
    for x in original:
        result_copy.remove(x)  # raises exception if element not found

    # the values should actually be sorted
    for k in range(1, len(result)):
        assert result[k - 1] <= result[k]


def check_student_sorting(original, result, key):
    """

    :param original: contains the array before sorting
    :param result: contains the output of the sorting algorithm
    :param key: attribute defining the order
    :return:
    """
    # both arrays should have same length
    assert len(original) == len(result)

    # all values of original array should still exist
    result_copy = list(result)
    for x in original:
        result_copy.remove(x)  # raises exception if element not found

    # the values should actually be sorted
    for k in range(1, len(result)):
        assert key(result[k - 1]) <= key(result[k])
        # if consecutive keys are the same, check stability
        if key(result[k - 1]) == key(result[k]):
            assert original.index(result[k - 1]) < original.index(result[k])


def check_nested_sorting(original, result):
    """

    :param original: contains the array before sorting
    :param result: contains the result of the sorting algorithm
    :return:
    """
    # both arrays should have same length
    assert len(original) == len(result)

    # all values of original array should still exist
    result_copy = list(result)
    for x in original:
        result_copy.remove(x)  # raises exception if element not found

    # the values should be sorted by mark
    for k in range(1, len(result)):
        assert result[k - 1].get_mark() <= result[k].get_mark()
        # if consecutive marks are the same, check that names are sorted
        if result[k - 1].get_mark() == result[k].get_mark():
            assert result[k - 1].get_name() <= result[k].get_name()
