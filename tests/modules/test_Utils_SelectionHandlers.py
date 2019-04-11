import sys
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import pytest
import unittest.mock as mock
import Utils , GAEngine , ChromosomeFactory


@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_basic(pop, fitness_dict, expected_results):
    
    #ga_mock = mock.Mock()

    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.basic(pop, fitness_dict, ga))) == list 


@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_random(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.random(pop, fitness_dict, ga))) == list 



@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_smallest(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.smallest(pop, fitness_dict, ga))) == list 



@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_largest(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.largest(pop, fitness_dict, ga))) == list 


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

@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_roulette(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.roulette(pop, fitness_dict, ga))) == list 


@pytest.mark.parametrize("pop, fitness_dict, expected_results", [
( [[1, 3, 4, 2], [3, 4, 1, 2]] , [([1, 3, 4, 2], 2), ([3, 4, 1, 2], 0)] ,  [1, 3, 4, 2])
])
def test_rank(pop, fitness_dict, expected_results):
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=4,minValue=1,maxValue=4)
    ga = GAEngine.GAEngine(factory,2,fitness_type=('equal',4),mut_prob = 0.3)
    #assert (Utils.SelectionHandlers.basic(pop, fitness_dict, ga)) == [1, 3, 4, 2]
    assert type((Utils.SelectionHandlers.rank(pop, fitness_dict, ga))) == list 



