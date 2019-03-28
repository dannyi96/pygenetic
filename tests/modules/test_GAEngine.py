import sys
import pytest
sys.path.append('../pyGenetic/')

import GAEngine,Utils


#@pytest.mark.parametrize([Utils.CrossoverHandlers.distinct, NOSUCHHANDLER])
def test_addCrossoverHandler():
    #ga = GAEngine()
    #ga.addCrossoverHandler(crossover_handler_param, 9)

    #assert ga.crossover_handlers[0] in dir(Utils.CrossoverHandlers)

    #if crossover_handler_param not in dir(Utils.CrossoverHandlers):
    #    assert NotImplementedError
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

def test_calculateFitness():
    pass

def test_generateFitnessDict():
    pass

def test_handle_selection():
    pass

def test_normalizeWeights():
    pass

def test_chooseCrossoverHandler():
    pass

def test_chooseMutationHandler():
    pass

def test_setEvolution():
    pass

def test_evolve():
    pass


if __name__ == '__main__':
    test_addCrossoverHandler()
    test_addMutationHandler()
    test_setCrossoverProbability()
    test_setMutationProbability()
    test_setSelectionHandler()
    test_setFitnessHandler()
    test_calculateFitness()
    test_generateFitnessDict()
    test_handle_selection()
    test_normalizeWeights()
    test_chooseCrossoverHandler()
    test_chooseMutationHandler()
    test_setEvolution()
    test_evolve()
