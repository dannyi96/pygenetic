import sys
sys.path.append('../pyGenetic/')

import ChromosomeFactory


def test_ChromosomeRegexFactory():

    factory = ChromosomeFactory.ChromosomeRegexFactory(int, noOfGenes=4,pattern='0|1|7')
    chromosome = factory.createChromosome()

    assert len(chromosome) == factory.noOfGenes
    assert factory.data_type is int


def test_ChromosomeRangeFactory():

    factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,3,11)
    chromosome = factory.createChromosome()

    assert len(chromosome) == factory.noOfGenes
    assert factory.minValue <= factory.maxValue

    if  factory.minValue > factory.maxValue :
        assert ValueError
    if factory.noOfGenes < 0:
        assert ValueError

if __name__ == '__main__':
    test_ChromosomeRegexFactory()
    test_ChromosomeRangeFactory()
