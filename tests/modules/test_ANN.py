from pygenetic import ANNEvolve
import numpy
import pytest

def test_ann():
	# load pima indians dataset
	dataset = numpy.loadtxt("examples/ANN_topology/input.csv", delimiter=",")
	# split into input (X) and output (Y) variables
	X = dataset[:,0:8]
	Y = dataset[:,8]
	a = ANNEvolve.ANNTopologyEvolve(X,Y,hiddenLayers=2)
	#a.evolve(1)
	assert type(a).__name__ == 'ANNTopologyEvolve'