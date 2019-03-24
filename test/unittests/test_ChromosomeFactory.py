import sys
sys.path.append('../pyGenetic/')

import ChromosomeFactory


def test_ChromosomeRegexFactory():

    factory = ChromosomeFactory.ChromosomeRegexFactory(int, noOfGenes=4,pattern='0|1|7')
    chromosome = factory.createChromosome()
    assert len(chromosome) == 4


def test_ChromosomeRangeFactory():
    pass


if __name__ == '__main__':
    test_ChromosomeRegexFactory()
