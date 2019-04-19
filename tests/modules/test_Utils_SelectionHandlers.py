import sys
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import pytest
import unittest.mock as mock
import Utils , GAEngine , ChromosomeFactory
from types import SimpleNamespace

@pytest.mark.parametrize("fitness_dict, expected_results", [
([([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_random(fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.random(fitness_dict, ga))) == list 



@pytest.mark.parametrize("fitness_dict, expected_results", [
( [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_smallest(fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.smallest(fitness_dict, ga))) == list 



@pytest.mark.parametrize("fitness_dict, expected_results", [
( [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_largest(fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.largest(fitness_dict, ga))) == list 


'''
@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_tournament(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.tournament(pop, fitness_dict, ga))) == list 
'''

@pytest.mark.parametrize("fitness_dict, expected_results", [
( [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_roulette(fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.roulette(fitness_dict, ga))) == list 


@pytest.mark.parametrize("fitness_dict, expected_results", [
(  [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_rank(fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.rank(fitness_dict, ga))) == list 



