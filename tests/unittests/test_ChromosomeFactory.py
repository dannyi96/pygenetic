import sys
sys.path.append('../pyGenetic/')

import ChromosomeFactory
import pytest

@pytest.mark.parametrize("data_type, noOfGenes, pattern ", [
    (int, 4,'0|1|7' ),
    (int, -1,'0|1|7'),
    (float, 4, '0|1|7'),
    (list, 4 , '0|1|7')
])
def test_ChromosomeRegexFactory(data_type, noOfGenes, pattern):

    factory = ChromosomeFactory.ChromosomeRegexFactory(data_type, noOfGenes, pattern)
    chromosome = factory.createChromosome()


    if factory.noOfGenes > 0:
        assert len(chromosome) == factory.noOfGenes
    assert factory.data_type == data_type

    if factory.noOfGenes < 0 :
        assert ValueError



@pytest.mark.parametrize("data_type, noOfGenes , minValue, maxValue", [
    (int, 4, 3 ,8),
    (int, -1, 8 ,3)
])
def test_ChromosomeRangeFactory(data_type, noOfGenes,  minValue, maxValue):

    factory = ChromosomeFactory.ChromosomeRangeFactory(data_type, noOfGenes, minValue, maxValue)
    chromosome = factory.createChromosome()

    if factory.noOfGenes > 0:
        assert len(chromosome) == factory.noOfGenes
    assert factory.minValue <= factory.maxValue

    if  factory.minValue > factory.maxValue :
        assert ValueError
    if factory.noOfGenes < 0:
        assert ValueError
'''
if __name__ == '__main__':
    test_ChromosomeRegexFactory()
    test_ChromosomeRangeFactory()
'''