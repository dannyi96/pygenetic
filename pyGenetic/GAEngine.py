import Population
import ChromosomeFactory
import random
import numpy as np
import collections
import Utils
import Evolution
import Statistics
import bisect

class GAEngine:

	def __init__(self,fitness_func,fitness_threshold,factory,population_size=100,cross_prob=0.8,mut_prob=0.1,fitness_type='max',adaptive_mutation=True,smart_fitness=False):
		self.fitness_func = fitness_func
		self.fitness_threshold = fitness_threshold
		self.factory = factory
		self.population = Population.Population(factory,population_size)
		self.population_size = population_size
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob
		#self.adaptive_mutation = adaptive_mutation
		self.smart_fitness = smart_fitness
		self.crossover_handlers = []
		self.crossover_handlers_weights = []
		self.mutation_handlers = []
		self.mutation_handlers_weights = []
		self.selection_handler = None
		self.fitness_type = fitness_type
		if self.fitness_type == 'max':
			self.best_fitness = None, float("-inf")
		elif self.fitness_type == 'min':
			self.best_fitness = None, float("inf")
		if adaptive_mutation == True:
			self.dynamic_mutation = None
		#elif self.fitness_type == 
		self.statistics = Statistics.Statistics()
		self.evolution = Evolution.StandardEvolution(100,adaptive_mutation=adaptive_mutation)

	def addCrossoverHandler(self,crossover_handler, weight = 1):
		self.crossover_handlers.append(crossover_handler)
		self.crossover_handlers_weights.append(weight)

	def addMutationHandler(self,mutation_handler, weight = 1):
		self.mutation_handlers.append(mutation_handler)
		self.mutation_handlers_weights.append(weight)

	def setCrossoverProbability(self,cross_prob):
		self.cross_prob = cross_prob

	def setMutationProbability(self,mut_prob):
		self.mut_prob = mut_prob

	def setSelectionHandler(self,selection_handler):
		self.selection_handler = selection_handler

	def calculateFitness(self,chromosome):
		return self.fitness_func(chromosome)

	def generateFitnessDict(self):
		self.fitness_dict = []
		for member in self.population.members:
			self.fitness_dict.append((member,self.fitness_func(member)))
			if self.fitness_type == 'max' and self.fitness_func(member) > self.best_fitness[1]:
				self.best_fitness = (member,self.fitness_func(member))
			elif self.fitness_type == 'min' and self.fitness_func(member) < self.best_fitness[1]:
				self.best_fitness = (member, self.fitness_func(member))

	def handle_selection(self):
		self.generateFitnessDict()
		return self.selection_handler(self.population.members,self.fitness_dict,self)
		
	def normalizeWeights(self):
		# Normalizing crossover and mutation handler weights, result is a CDF
		total = sum(self.mutation_handlers_weights)
		cumsum = 0
		for i in range(len(self.mutation_handlers_weights)):
			cumsum += self.mutation_handlers_weights[i]
			self.mutation_handlers_weights[i] = cumsum/total
		print("mutation_handlers_weights = ",self.mutation_handlers_weights)
		total = sum(self.crossover_handlers_weights)
		cumsum = 0
		for i in range(len(self.crossover_handlers_weights)):
			cumsum += self.crossover_handlers_weights[i]
			self.crossover_handlers_weights[i] = cumsum/total
		print("crossover_handlers_weights = ",self.crossover_handlers_weights)
			
	def chooseCrossoverHandler(self):
		x = random.random()
		idx = bisect.bisect(self.crossover_handlers_weights, x)
		return self.crossover_handlers[idx]

	def chooseMutationHandler(self):
		x = random.random()
		idx = bisect.bisect(self.mutation_handlers_weights, x)
		return self.mutation_handlers[idx]

	def evolve(self,noOfIterations=50):
		self.normalizeWeights()
		for i in range(noOfIterations):
			result = self.evolution.evolve(self)
			self.statistics.compute(ga.best_fitness[1])
			if result:
				print('SOLVED')
				self.statistics.plot()
				break


if __name__ == '__main__':
	#factory = ChromosomeFactory.ChromosomeRegexFactory(int,noOfGenes=4,pattern='0|1')
	#ga = GAEngine(lambda x:sum(x),'MAX',factory,20)
	#print(ga.fitness_func)
	#print(ga.fitness_type)
	#ga.calculateAllFitness()
	import copy
	factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,1,9)
	def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness

	ga = GAEngine(fitness,8,factory,100)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 9)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 3)
	ga.addMutationHandler(Utils.MutationHandlers.swap)
	ga.setSelectionHandler(Utils.SelectionHandlers.basic)
	ga.evolve(100)
