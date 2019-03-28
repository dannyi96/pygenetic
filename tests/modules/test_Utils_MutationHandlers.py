import sys
sys.path.append('../../pyGenetic/')
import pytest
import Utils

@pytest.mark.parametrize("chromosome,expected_results", [
( [0,1], [[1,0]] ),
( [1,2,3], [[1,3,2],[2,1,3]]),
( [1,2,3,4], [[2,1,3,4],[1,3,2,4],[1,2,4,3]] )
])
def test_swap(chromosome,expected_results):
    assert Utils.MutationHandlers.swap(chromosome) in expected_results


def test_bitFlip():
    pass




if __name__ == '__main__':
    test_swap()
    test_bitFlip()
