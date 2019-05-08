from pygenetic.ChromosomeFactory import *
from pygenetic import Utils, GAEngine
from keras.models import Sequential
from keras.layers import Dense
import numpy
import random
import copy

class ANNTopologyChromosomeFactory(ChromosomeFactory):
	"""
	ChromosomeFactory Class used to create ANN Chromosomes

	Instance variables :
	------------------
	neuronsPerLayer : list of possible number of neurons in the ANN to be used
	activations: list of possible number of activations to be used in ANN
	optimizers: list of possible number of optimizers to be used in ANN
	hiddenLayers: number of hidden layers to be used in the ANN(fixed)

	Methods :
	---------
	createChromosome() : method to be create ANN chromosome

	"""
	def __init__(self,hiddenLayers,neuronsPerLayer,activations,optimizers):
		self.neuronsPerLayer = neuronsPerLayer
		self.activations = activations
		self.optimizers = optimizers
		self.hiddenLayers = hiddenLayers

	def createChromosome(self):
		"""
		Generates ANN chromosome
		
		"""
		chromosome = []
		for i in range(self.hiddenLayers):
			chromosome.extend([random.choice(self.neuronsPerLayer), random.choice(self.activations)])
		chromosome.append(random.choice(self.activations))
		chromosome.append(random.choice(self.optimizers))
		return chromosome

class ANNTopologyEvolve:
	"""
	Class used to find best ANN topology using GA

	Instance variables :
	------------------
	X,Y: input and output values for ANN to train on
	population_size: GA population size
	loss: ANN loss to be used(eg:'binary_crossentropy')
	metrics: ANN metrics to be used (eg:'accuracy')
	epochs: Number of ANN epochs
	batch_size: ANN Batch size  
	neuronsPerLayer : list of possible number of neurons in the ANN to be used
	activations: list of possible number of activations to be used in ANN
	optimizers: list of possible number of optimizers to be used in ANN
	hiddenLayers: number of hidden layers to be used in the ANN(fixed)

	Methods :
	---------
	evolve(noOfGenerations) : used to find best ANN topology using GA evolutions

	"""
	def __init__(self,X,Y,hiddenLayers,population_size=10,neuronsPerLayer=[2,5,10,12],activations=['relu','sigmoid'],optimizers=['adam'],loss='binary_crossentropy',metrics='accuracy',epochs=30,batch_size=10):
		self.X = X
		self.Y = Y
		if hiddenLayers < 1:
			raise Exception('No of hiddenLayers should be greater than zero')
		self.hiddenLayers = hiddenLayers
		self.input_dim = len(X[0])
		self.neuronsPerLayer = neuronsPerLayer
		self.activations = activations
		self.optimizers = optimizers
		self.loss = loss
		self.metrics = metrics
		self.epochs = epochs
		self.batch_size = batch_size
		self.population_size = population_size
		self.factory = ANNTopologyChromosomeFactory(hiddenLayers,neuronsPerLayer,activations,optimizers)

	def evolve(self,noOfGenerations=100):
	"""
	Function to evolve the ANN Topology finder Genetic Algorithm

	Parameters :
	---------
	noOfGenerations : number of generations to evolve the GA

	"""
		ga = GAEngine.GAEngine(self.factory,population_size=self.population_size,fitness_type='min')
		ga.setFitnessHandler(ANNTopologyEvolve.fitness,self.X,self.Y,self.hiddenLayers,self.input_dim,self.loss,self.metrics,self.epochs,self.batch_size)
		ga.setSelectionHandler(Utils.SelectionHandlers.best)
		ga.addCrossoverHandler(Utils.CrossoverHandlers.onePoint,1)
		ga.addMutationHandler(ANNTopologyEvolve.mutation,1,self.neuronsPerLayer,self.activations,self.optimizers)
		ga.evolve(noOfGenerations)

	@staticmethod
	def fitness(chromosome,X,Y,hidden_layers,input_dim,loss,metrics,epochs,batch_size):
	"""
	Function to calculate the ANN fitness(loss value) given chromosome and other ANN inputs
	"""
		# create model
		model = Sequential()
		model.add(Dense(chromosome[0], input_dim= input_dim, activation=chromosome[1]))
		for i in range(hidden_layers-1):
			model.add(Dense(chromosome[i+2], activation=chromosome[i+3]))
		model.add(Dense(1, activation=chromosome[len(chromosome)-2]))
		# Compile model
		model.compile(loss=loss, optimizer=chromosome[len(chromosome)-1], metrics=[metrics])
		# Fit the model
		model.fit(X, Y, epochs=epochs, batch_size=batch_size,verbose=1)
		# evaluate the model
		scores = model.evaluate(X, Y)
		print(scores)
		print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
		print('Loss', scores[0])
		return scores[0]

	@staticmethod
	def mutation(chromosome,neuronsPerLayer,activations,optimizers):
	"""
	Function to mutate the ANN chromosome
	"""
		r = random.randint(0,len(chromosome)-1)
		newchrom = copy.copy(chromosome)
		if r == len(chromosome) - 1:
			newchrom[r] = random.choice(optimizers)
		elif r%2 == 1 or r == len(chromosome)-2:
			newchrom[r] = random.choice(activations)
		elif r%2 == 0:
			newchrom[r] = random.choice(neuronsPerLayer)
		return newchrom
