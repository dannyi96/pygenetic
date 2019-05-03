from pygenetic import ChromosomeFactory, Population
import pytest


@pytest.mark.parametrize("population_size", [
( 2 ),
( 3 ),
( 7 )
])
def test_create_members(population_size):
	factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=4,minValue=1,maxValue=4)
	population = Population.Population(factory,population_size)
	assert len(population.members) == population_size
    