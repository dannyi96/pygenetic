import GAEngine
from ChromosomeFactory import *
from keras.models import Sequential
from keras.layers import Dense
import numpy
import random
import Utils
# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
dataset = numpy.loadtxt("input.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]

class ANNChromosomeFactory(ChromosomeFactory):
	def __init__(self,neuronsPerLayer,activations,optimizers):
		self.neuronsPerLayer = neuronsPerLayer
		self.activations = activations
		self.optimizers = optimizers

	def createChromosome(self):
		return [random.choice(self.neuronsPerLayer), random.choice(self.activations), random.choice(self.neuronsPerLayer), random.choice(self.activations), random.choice(self.optimizers)]


class ANNEvolve:
	def __init__(self,X,Y,neuronsPerLayer=[2,5,10,12],activations=['relu','sigmoid'],optimizers=['adam'],loss='binary_crossentropy',metrics='accuracy'):
		self.X = X
		self.Y = Y
		self.input_dim = len(X[0])
		self.neuronsPerLayer = neuronsPerLayer
		self.activations = activations
		self.optimizers = optimizers
		self.loss = loss
		self.metrics = metrics
		self.factory = ANNChromosomeFactory(neuronsPerLayer,activations,optimizers)
		print(self.factory.createChromosome())
		#self.fitness(self.factory.createChromosome(),self.input_dim,self.loss,self.metrics)

	def new_evolve(self):
		ga = GAEngine.GAEngine(self.factory,population_size=10,fitness_type='min')
		ga.setFitnessHandler(ANNEvolve.fitness,self.input_dim,self.loss,self.metrics)
		ga.setSelectionHandler(Utils.SelectionHandlers.best)
		ga.evolve(1)

	@staticmethod
	def fitness(chromosome,input_dim,loss,metrics):
		# create model
		model = Sequential()
		model.add(Dense(chromosome[0], input_dim= input_dim, activation=chromosome[1]))
		model.add(Dense(chromosome[2], activation=chromosome[3]))
		model.add(Dense(1, activation='sigmoid'))
		# Compile model
		model.compile(loss=loss, optimizer=chromosome[4], metrics=[metrics])
		# Fit the model
		model.fit(X, Y, epochs=30, batch_size=10)
		# evaluate the model
		scores = model.evaluate(X, Y)
		print(scores)
		print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		print('Loss', scores[0])
		return scores[0]

if __name__ == '__main__':
	a = ANNEvolve(X,Y)
	a.new_evolve()
	#a.evolve()
