import sys
sys.path.append('../../pyGenetic/')

import Utils
import unittest.mock as mock
import random
import pytest

@pytest.mark.parametrize("chromosome1,chromosome2,random_index,expected_children", [
([1,2,3,4], [4,1,2,3], 2, ([1,2,4,3],[4,1,2,3])),
([1,2,3,4,5,6,7,8,9,10], [4,1,2,3,5,8,7,6,9,10], 5, ([1,2,3,4,5,8,7,6,9,10],[4,1,2,3,5,6,7,8,9,10]))
])
def test_distinct(chromosome1,chromosome2,random_index,expected_children):
    with mock.patch('random.randint', lambda x,y:random_index):
        assert Utils.CrossoverHandlers.distinct(chromosome1,chromosome2) == expected_children
     


def test_onePoint():
    pass

def test_twoPoint():
    pass

def test_PMX():
    pass

def test_OX():
    pass




if __name__ == '__main__':
    test_distinct()
    test_onePoint()
    test_twoPoint()
    test_PMX()
    test_OX()
