from pygenetic import ChromosomeFactory
import pytest
import re

@pytest.mark.parametrize("noOfGenes, pattern, data_type", [
( -1,'0|1|7',int),
( 0, '0|1|7',float),
( 4 , '0|1|7',list),
(5,'0[',int),
(10,'a.d|b.d|c.d',int)
])
def test_errors_ChromosomeRegexFactory(noOfGenes, pattern, data_type):
    # Test case 1: Test for exception when no of genes less than or equal to 0
    if noOfGenes<=0:
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRegexFactory(noOfGenes, pattern, data_type)
        return

    # Test case 2: Test for exception when invalid data type is given
    if data_type not in [float,int,str]:
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRegexFactory(noOfGenes, pattern, data_type)
            
    # Test case 3: Test for exception when invalid regex is given
    try:
        re.compile(pattern)
    except:
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRegexFactory(noOfGenes, pattern, data_type)
        return

    # Test case 4: Test errors for invalid regex type conversion
    if data_type == int or data_type == float:
        factory = ChromosomeFactory.ChromosomeRegexFactory(noOfGenes,pattern,data_type)
        # Test only when conversion is not possible
        try:
            result = data_type(factory.createChromosome())
        except:
            with pytest.raises(Exception):
                factory.createChromosome()

@pytest.mark.parametrize("noOfGenes, pattern, data_type", [
(3,'a|b|x',str),
(10,'1|0|7',int)
])
def test_functionality_ChromosomeRegexFactory(noOfGenes, pattern, data_type):
    
    factory = ChromosomeFactory.ChromosomeRegexFactory(noOfGenes=noOfGenes,pattern=pattern,data_type=data_type)
    chromosome = factory.createChromosome()
    
    # Test case 5: Check if correct no of genes are produced
    assert len(chromosome) == noOfGenes

    # Test case 6: Check if correct genes are produced from regex
    for gene in chromosome:
        pattern_regex = re.compile(pattern)
        assert pattern_regex.match(str(gene))


'''
if __name__ == '__main__':
    test_ChromosomeRegexFactory()
    test_ChromosomeRangeFactory()
'''

@pytest.mark.parametrize("noOfGenes, minVal, maxVal, duplicates", [
( 1, 2 , 100 ,False),
(-1 ,3 ,100,False),
(2, 0, -9 ,False),
(2, 0, 9 , int),
(3, 0 , 9, True)
])
def test_errors_ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates):
    # Test case 7: Test for exception when no of genes less than or equal to 0
    if noOfGenes<=0:
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates)
        return
         
    # Test case 8: Test for exception when invalid range is given
    if minVal > maxVal:    
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates)
        return

    # Test case 9: Test errors for invalid duplicates type
    if type(duplicates) != bool:
        with pytest.raises(ValueError):
            factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates)
        return


@pytest.mark.parametrize("noOfGenes, minVal, maxVal, duplicates", [
( 3, 2 , 10 ,False)

])
def test_functionality_ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates):
    
    factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes, minVal, maxVal, duplicates)
    chromosome = factory.createChromosome()
    
    # Test case 11: Check if correct no of genes are produced
    assert len(chromosome) == noOfGenes

    # Test case 12: Check if correct genes are produced from regex
    for gene in chromosome:
        assert gene >= minVal and gene <= maxVal

