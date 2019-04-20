import sys
sys.path.append('../../pyGenetic/')
sys.path.append('../pyGenetic/')
sys.path.append('./pyGenetic/')
sys.path.append('.')

import SimpleGA
import pytest

@pytest.mark.parametrize("minValue, maxValue, noOfGenes, duplicates, population_size,crossover_handler,mutation_handler,selection_handler,fitness_type", [
(1,10,12,True,100,'distinct','swap','best','max'),
(1,32,20,False,100,'onePoint','swap','best','max'),
(1,10,12,True,100,'twoPoint','bitFlip','roulette','min'),
(1,32,20,False,100,'PMX','bitFlip','rank','min'),
(1,10,12,True,100,'OX','bitFlip','rank',('equal',8)),
])
def test_simple_ga(minValue, maxValue, noOfGenes, duplicates, population_size,crossover_handler,mutation_handler,selection_handler,fitness_type):
	ga = SimpleGA.SimpleGA(minValue=minValue,maxValue=maxValue,noOfGenes=noOfGenes,fitness_func=lambda x:sum(x),duplicates=duplicates,population_size=population_size,fitness_type='max')
	assert ga.minValue == minValue
	assert ga.maxValue == maxValue
	assert ga.noOfGenes == noOfGenes
	assert ga.duplicates == duplicates
	assert ga.population_size == population_size
	ga.generateFitnessMappings()
	assert ga.fitness_mappings
	ga.evolve(1)
	assert type(ga.best_fitness[0]) == list
	assert type(ga.best_fitness[1]) == int

@pytest.mark.parametrize("minValue, maxValue, noOfGenes, duplicates, population_size,crossover_handler,mutation_handler,selection_handler,fitness_type", [
(1,10,12,True,100,'distinct','junk','best','max'),
(1,32,20,False,100,'onePoint','swap','invalud','max'),
(1,10,12,True,100,'twoPoint','bitFlip','roulette','junk'),
(1,32,20,False,100,'lollipop','bitFlip','rank','min'),
(1,10,12,True,100,'OX','bitFlip','rank','you'),
])
def test_errors(minValue, maxValue, noOfGenes, duplicates, population_size,crossover_handler,mutation_handler,selection_handler,fitness_type):
	ga = SimpleGA.SimpleGA(minValue=minValue,maxValue=maxValue,noOfGenes=noOfGenes,fitness_func=lambda x:sum(x),duplicates=duplicates,population_size=population_size,fitness_type='max')
	with pytest.raises(Exception):
		ga.doCrossover()
		ga.doMutation()
		ga.handle_selection()