import ANNEvolve 
import numpy
# load pima indians dataset
dataset = numpy.loadtxt("input.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
print(X)
a = ANNEvolve.ANNTopologyEvolve(X,Y,hiddenLayers=2)
a.evolve(2)
#print(a.best_fitness)