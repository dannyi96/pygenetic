import sys
import pytest
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import GAEngine,Utils,ChromosomeFactory

def select_all(fitness_mappings, ga):
        return [i[0] for i in fitness_mappings]

def test_true_population_control():
    # Verify when population control is True
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=1,maxValue=100)
    ga = GAEngine.GAEngine(factory,population_size=100,fitness_type='max',mut_prob = 0.3,population_control = True)
    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(select_all)
    ga.setFitnessHandler(lambda x:sum(x))
    ga.evolve(1)
    assert len(ga.population.members) == 100


def test_false_population_control():
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=1,maxValue=100)
    ga = GAEngine.GAEngine(factory,population_size=100,fitness_type='max',mut_prob = 0.3,population_control = False)
    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(select_all)
    ga.setFitnessHandler(lambda x:sum(x))
    ga.evolve(1)
    assert len(ga.population.members) > 100






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
    '''
    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=14,minValue=1,maxValue=15)
    ga = GAEngine.GAEngine(factory,100,fitness_type=('equal',14),mut_prob = 0.3)
    ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
    ga.addMutationHandler(Utils.MutationHandlers.swap)
    ga.setSelectionHandler(Utils.SelectionHandlers.largest)
    ga.setFitnessHandler(fitness)


    with pytest.raises(ValueError):
        ga.generateFitnessDict()
    '''
    pass
    
def test_normalizeWeights():
    pass

def test_chooseCrossoverHandler():
    pass

def test_chooseMutationHandler():
    pass

def test_evolve():
    pass
