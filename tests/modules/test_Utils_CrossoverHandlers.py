from pygenetic import Utils

import pytest
import unittest.mock as mock
import random

@pytest.mark.parametrize("chromosome1,chromosome2,random_index,expected_children", [
([1,2,3,4], [4,1,2,3], 2, ([1,2,4,3],[4,1,2,3])),
([1,2,3,4,5,6,7,8,9,10], [4,1,2,3,5,8,7,6,9,10], 5, ([1,2,3,4,5,8,7,6,9,10],[4,1,2,3,5,6,7,8,9,10]))
])
def test_mock_distinct(chromosome1,chromosome2,random_index,expected_children):
    with mock.patch('random.randint', lambda x,y:random_index):
        assert Utils.CrossoverHandlers.distinct(chromosome1,chromosome2) == expected_children
     
@pytest.mark.parametrize("chromosome1,chromosome2,random_index,expected_children", [
([1,2,3,4], [4,1,2,3], 2, ([1,2,2,3],[4,1,3,4])),
([1,2,3,4,5,6,7,8,9,10], [4,1,2,3,5,8,7,6,9,10], 5, ([1,2,3,4,5,8,7,6,9,10],[4,1,2,3,5,6,7,8,9,10]))
])
def test_mock_onePoint(chromosome1,chromosome2,random_index,expected_children):
    with mock.patch('random.randint', lambda x,y:random_index):
        assert Utils.CrossoverHandlers.onePoint(chromosome1,chromosome2) == expected_children

@pytest.mark.parametrize("chromosome1,chromosome2,expected_children", [
([1,2,3,4], [5,6,7,8], [([1,2,3,8],[5,6,7,4]), ([1,2,7,8],[5,6,3,4]), ([1,6,7,8],[5,2,3,4])] ),
([1,2,3,4,5], [6,7,8,9,10], [([1,2,3,4,10],[6,7,8,9,5]), ([1,2,3,9,10],[6,7,8,4,5]), ([1,2,8,9,10],[6,7,3,4,5]), ([1,7,8,9,10],[6,2,3,4,5])] )
])
def test_onePoint(chromosome1,chromosome2,expected_children):
    assert Utils.CrossoverHandlers.onePoint(chromosome1,chromosome2) in expected_children


@pytest.mark.parametrize("chromosome1,chromosome2,expected_children", [
([1,2,3,4], [5,6,7,8], [([1,2,3,8],[5,6,7,4]), ([1,2,7,8],[5,6,3,4]), ([1,6,7,8],[5,2,3,4])] ),
([1,2,3,4,5], [6,7,8,9,10], [([1,2,3,4,10],[6,7,8,9,5]), ([1,2,3,9,10],[6,7,8,4,5]), ([1,2,8,9,10],[6,7,3,4,5]), ([1,7,8,9,10],[6,2,3,4,5])] )
])
def test_twoPoint(chromosome1,chromosome2,expected_children):
    assert Utils.CrossoverHandlers.onePoint(chromosome1,chromosome2) in expected_children

def test_twoPoint():
    pass

def test_PMX():
    pass

def test_OX():
    pass
