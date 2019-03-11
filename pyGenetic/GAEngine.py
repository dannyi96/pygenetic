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

	def __init__(self,fitness_threshold,factory,population_size=100,cross_prob=0.8,mut_prob=0.1,fitness_type='max',adaptive_mutation=True,smart_fitness=False, tournsize = 3):
		self.fitness_func = None
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
		elif self.fitness_type == 'equal':	# Fitness must be absolute difference between member score and fitness_threshold
			self.best_fitness = None, float("inf") 
		if adaptive_mutation == True:
			self.dynamic_mutation = None
		#elif self.fitness_type == 
		self.statistics = Statistics.Statistics()
		self.evolution = Evolution.StandardEvolution(100,adaptive_mutation=adaptive_mutation)
		self.fitness_external_data = []

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
		
	def setFitnessHandler(self, fit_function, *args):
		self.fitness_func = fit_function
		for arg in args:
			self.fitness_external_data.append(arg)

	def calculateFitness(self,chromosome):
		if self.fitness_external_data:
			return self.fitness_func(chromosome, *(self.fitness_external_data))
		else:
			return self.fitness_func(chromosome)

	def generateFitnessDict(self):
		self.fitness_dict = []
		for member in self.population.members:
			this_member_fitness = self.calculateFitness(member)
			self.fitness_dict.append((member, this_member_fitness))
			if self.fitness_type == 'max' and this_member_fitness > self.best_fitness[1]:
				self.best_fitness = (member,this_member_fitness)
			elif self.fitness_type == 'min' and this_member_fitness < self.best_fitness[1]:
				self.best_fitness = (member, this_member_fitness)
			elif self.fitness_type == 'equal' and abs(this_member_fitness-self.fitness_threshold) < abs(self.best_fitness[1]-self.fitness_threshold):
				self.best_fitness = (member, this_member_fitness)

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
	factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,0,8)
	'''def fitness(board):
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
		return fitness'''
		
	matrix = [[0,172,145,607,329,72,312,120],[172,0,192,494,209,158,216,92],[145,192,0,490,237,75,205,100],[607,494,490,0,286,545,296,489],[329,209,237,286,0,421,49,208],[72,158,75,545,421,0,249,75],[312,216,205,296,49,249,9,194],[120,92,100,489,208,75,194,0]]
	# best sequence i found: 0 5 2 7 1 6 4 3

	ga = GAEngine(8,factory,100,fitness_type='min',mut_prob = 0.5)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 9)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 3)
	ga.addMutationHandler(Utils.MutationHandlers.swap)
	ga.setSelectionHandler(Utils.SelectionHandlers.SUS)
	ga.setFitnessHandler(Utils.Fitness.TSP, matrix)
	ga.evolve(100)
