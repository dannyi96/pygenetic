import sys
import pytest
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import GAEngine,Utils,ChromosomeFactory


#Getters and Setters need not be tested
#https://stackoverflow.com/questions/6197370/should-unit-tests-be-written-for-getter-and-setters
'''
def test_addCrossoverHandler():
    pass

def test_addMutationHandler():
    pass

def test_setCrossoverProbability():
    pass

def test_setMutationProbability():
    pass

def test_setSelectionHandler():
    pass

def test_setFitnessHandler():
    pass
'''

@pytest.mark.parametrize("chromosome,expected_results", [
([14,13,12,10,9,8,7,6,5,4,3,2,1],14),
])
def test_calculateFitness(chromosome,expected_results):
    '''
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=14,minValue=1,maxValue=15)
    ga = GAEngine.GAEngine(factory,100,fitness_type=('equal',14),mut_prob = 0.3)

    assert ga.calculateFitness(chromosome) in expected_results
    '''
    pass
    
def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness



def test_generateFitnessDict():
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=14,minValue=1,maxValue=15)
    ga = GAEngine.GAEngine(factory,100,fitness_type=('equal',14),mut_prob = 0.3)
    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(Utils.SelectionHandlers.largest)
    ga.setFitnessHandler(fitness)


    with pytest.raises(ValueError):
        ga.generateFitnessDict()

    
def test_normalizeWeights():
    pass

def test_chooseCrossoverHandler():
    pass

def test_chooseMutationHandler():
    pass

def test_evolve():
    pass
