from pygenetic import Population, Evolution, Statistics
import random
import collections
import bisect
import math
import numpy as np

class GAEngine:
	"""This Class is the main driver program which contains and invokes the operators used in Genetic algorithm

	GAEngine keeps track of specific type of operators the user has specified for running the algorithm

	Methods
	---------
	addCrossoverHandler(crossover_handler, weight)
		Sets the function to be used for crossover operation

	addMutationHandler(mutation_handler, weight)
		Sets the function to be used for mutation operation

	setCrossoverProbability(cross_prob)
		Sets value for cross_prob instance variable for crossover operation

	setMutationProbability(mut_prob)
		Sets value for mut_prob instance variable

	setSelectionHandler(selection_handler)
		Sets the function to be used for selection operation

	calculateFitness(chromosome)
		Invokes fitness function (fitness_func) to compute the fitness score of a chromosome

	generateFitnessDict()
		Generates a  dictionary of (individual, fitness_score) and also stores the dictionary
		containing fittest chromosome depending on fitness_type(max/min/equal)

	handle_selection()
		Invokes generateFitnessDict() and  selection_handler specified

	normalizeWeights()
		Normalizes crossover and mutation handler weights, result is a CDF

	chooseCrossoverHandler()
		Selects crossover handler from available handlers based on weightage given to handlers

	chooseMutationHandler()
		Selects mutation handler from available handlers based on weightage given to handlers

	evolve()
		Invokes evolve method in Evolution module  which Executes the operations of Genetic algorithm till
		a fitness score reaches a threshold or the number of iterations reach max iterations specified by user


	Instance Members
	-----------
	fitness_func : A function argument
				The fitness function to be used, passed as a function argument

	fitness_threshold : int
				Threshold at which a candidate solution is considered optimal solution to the problem

	factory : Instance of any subclass of ChromosomeFactory class
				Generates and returns the initial population of candidate solutions

	population_size : int
				The number of candidate solutions that can exist after every iteration

	cross_prob : float
				The Crossover probability of crossover operation which determines the extent to which crossover between parents

	mutation_prob : float
				The mutation probability of mutation operation which determines extent to which candidates should be mutated

	fitness_type : string
				Indicates the nature of fitness value (higher/lower/equal) to be considered during selection of candidates
				(default is max)

	adaptive_mutation : boolean
				If set rate of mutation of candidates dynamically changes during execution depending on diversity in population
				(default is true)

	smart_fitness : boolean
				TO BE DESCRIBED

  	"""


	def __init__(self,factory,population_size=100,cross_prob=0.7,mut_prob=0.1,fitness_type='max',adaptive_mutation=True, population_control=False,hall_of_fame_injection=True,efficient_iteration_halt=True,use_pyspark=False):
		self.fitness_func = None
		self.factory = factory
		self.cross_prob = cross_prob
		self.adaptive_mutation = adaptive_mutation
		if self.adaptive_mutation:
			self.initial_mut_prob = mut_prob
		else:
			self.mut_prob = mut_prob
		self.crossover_handlers = []
		self.crossover_handlers_weights = []
		self.mutation_handlers = []
		self.mutation_handlers_weights = []
		self.selection_handler = None
		self.fitness_type = fitness_type
		self.fitness_mappings = None
		self.population = None
		self.population_size = population_size
		if type(self.fitness_type) == str:
			if self.fitness_type == 'max':
				self.best_fitness = None, float("-inf")
			elif self.fitness_type == 'min':
				self.best_fitness = None, float("inf")
			else:
				raise Exception('Invalid Fitness Type given to GAEngine')
		elif type(self.fitness_type) == tuple or type(self.fitness_type) == list:
			if self.fitness_type[0] == 'equal':
				self.best_fitness = None, float("inf")
		else:
			raise Exception('Invalid Fitness Type given to GAEngine')
		self.evolution = Evolution.StandardEvolution(pyspark=use_pyspark)
		self.population_control = population_control
		self.hall_of_fame_injection = hall_of_fame_injection
		self.efficient_iteration_halt = efficient_iteration_halt
		self.fitness_external_data = []
		self.selection_external_data = []
		self.crossover_external_data = {}
		self.mutation_external_data = {}
		self.hall_of_fame = None
		self.extra_statistics = {}

	def addCrossoverHandler(self,crossover_handler, weight = 1, *args):
		"""
		Adds crossover handler staticmethod defined in Utils.py and
		appends the weightage to be given to the handler

		Parameters :
		----------
		crossover_handler : Method defined in Utils.py
		weight : int

		"""

		self.crossover_handlers.append(crossover_handler)
		self.crossover_handlers_weights.append(weight)
		xtra_args = []
		for arg in args:
			xtra_args.append(arg)
		self.crossover_external_data.update({crossover_handler:tuple(xtra_args)})

			

	def addMutationHandler(self,mutation_handler, weight = 1, *args):
		"""
		Adds mutation handler staticmethod defined in Utils.py and
		appends the weightage to be given to the handler

		Parameters :
		----------
		mutation_handler : Method defined in Utils.py
		weight : int

		"""

		self.mutation_handlers.append(mutation_handler)
		self.mutation_handlers_weights.append(weight)
		xtra_args = []
		for arg in args:
			xtra_args.append(arg)
		self.mutation_external_data.update({mutation_handler:tuple(xtra_args)})

	def doCrossover(self, cross_func, member1, member2):
		if cross_func in self.crossover_external_data:
			return cross_func(member1, member2, *(self.crossover_external_data[cross_func]))
		else:
			return cross_func(member1, member2)

	def doMutation(self, mut_func, member):
		if mut_func in self.mutation_external_data:
			return mut_func(member, *(self.mutation_external_data[mut_func]))
		else:
			return mut_func(member)

	def setSelectionHandler(self,selection_handler, *args):
		"""
		Sets function to be used for selection_handler

		Parameters:
		----------
		Function to be used for selection_handler

		"""
		self.selection_handler = selection_handler
		for arg in args:
			self.selection_external_data.append(arg)

	def setFitnessHandler(self, fit_function, *args):
		self.fitness_func = fit_function
		for arg in args:
			self.fitness_external_data.append(arg)

	def calculateFitness(self,chromosome):
		"""
		Invokes fitness function (fitness_func) to compute the fitness score of a chromosome

		Parameters:
		----------
		chromosome for which fitness is to be calculated

		Returns:
		--------
		Fitness value of chromosome

		"""
		if self.fitness_external_data:
			return self.fitness_func(chromosome, *(self.fitness_external_data))
		else:
			return self.fitness_func(chromosome)

	def generateFitnessMappings(self):
		"""
		Generates a  dictionary of (individual, fitness_score) and also stores the dictionary
		containing fittest chromosome depending on fitness_type(max/min/equal)

		"""

		self.fitness_mappings = [(member, self.calculateFitness(member)) for member in self.population.members]
		if type(self.fitness_type) == str:
			if self.fitness_type == 'max':
				self.fitness_mappings.sort(key=lambda x:x[1],reverse=True)
				self.best_fitness = self.fitness_mappings[0]
				if self.hall_of_fame:
					if self.best_fitness[1] > self.hall_of_fame[1]:
						self.hall_of_fame = self.best_fitness
				else:
					self.hall_of_fame = self.best_fitness

			elif self.fitness_type == 'min':
				self.fitness_mappings.sort(key=lambda x:x[1])
				self.best_fitness = self.fitness_mappings[0]
				if self.hall_of_fame:
					if self.best_fitness[1] < self.hall_of_fame[1]:
						self.hall_of_fame = self.best_fitness
				else:
					self.hall_of_fame = self.best_fitness

		elif type(self.fitness_type) == tuple or type(self.fitness_type) == list:
			self.fitness_mappings.sort(key=lambda x:abs(x[1]-self.fitness_type[1]))
			self.best_fitness = self.fitness_mappings[0]
			if self.hall_of_fame:
				if abs(self.fitness_type[1] - self.best_fitness[1]) < abs(self.fitness_type[1] - self.hall_of_fame[1]):
					self.hall_of_fame = self.best_fitness
			else:
				self.hall_of_fame = self.best_fitness

	def handle_selection(self,repeat_chromosome_sorting=False):

		"""
		Invokes generateFitnessDict() to generate dictionary of (chromosome,fitness)
		Invokes selection_handler staticmethod defined in Utils.py module

		Returns :
		---------
		List of  fittest members of population

		"""
		if repeat_chromosome_sorting:
			self.generateFitnessMappings()
		if self.selection_external_data:
			return self.selection_handler(self.fitness_mappings,self, *(self.selection_external_data))
		else:
			return self.selection_handler(self.fitness_mappings,self)

	def normalizeWeights(self):
		"""
		Normalizes the weights of mutation and crossover handlers

		"""

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
		"""
		Selects crossover handler from available handlers based on weightage given to handlers

		Returns :
		--------
		The selected crossover handler function

		"""

		x = random.random()
		idx = bisect.bisect(self.crossover_handlers_weights, x)
		return self.crossover_handlers[idx]

	def chooseMutationHandler(self):
		"""
		Selects mutation handler from available handlers based on weightage given to handlers

		Returns :
		--------
		The selected mutation handler function

		"""

		x = random.random()
		idx = bisect.bisect(self.mutation_handlers_weights, x)
		return self.mutation_handlers[idx]

	def setEvolution(self,evolution):
		self.evolution = evolution

	def addStatistic(self,statistic,statistic_function):
		if type(statistic) != str:
			raise Exception('Invalid Statistics key')
		self.extra_statistics[statistic] = statistic_function

	def evolve(self,noOfIterations=50):
		"""
		Performs the evolution by invoking the evolve method from Evolution.py module
		as many times as number of iterations specified by user or terminates if optimal
		solution is found.
		Also invokes compute method from Statistics.py module to generate graph

		Parameters :
		-----------
		noOfIterations : int
						default value : 50

		"""
		self.population = Population.Population(self.factory,self.population_size)
		self.statistics = Statistics.Statistics()
		self.last_20_fitnesses = collections.deque([])
		self.continue_evolve(noOfIterations)
		
	def continue_evolve(self, noOfIterations=20):
		self.normalizeWeights()
		if self.population == None:
			raise Exception('Call evolve before calling continue_evolve')
		for i in range(noOfIterations):
			self.generateFitnessMappings()
			fitnesses = [ x[1] for x in self.fitness_mappings]
			self.statistics.add_statistic('best-fitness',self.fitness_mappings[0][1])
			self.statistics.add_statistic('worst-fitness',self.fitness_mappings[-1][1])
			self.mean_fitness = sum(fitnesses)/len(fitnesses)
			self.statistics.add_statistic('avg-fitness',self.mean_fitness)
			self.diversity = math.sqrt(sum((fitness - self.mean_fitness)**2 for fitness in fitnesses)) / len(fitnesses)
			if self.adaptive_mutation:
				self.mut_prob = self.initial_mut_prob * ( 1 + ((self.best_fitness[1]-self.diversity) / (self.diversity+self.best_fitness[1]) ) )
				self.mut_prob = np.clip(self.mut_prob,0.0001,0.8)
				print("Diversity = ",self.diversity)
				print('New mutation value = ',self.mut_prob)
			self.statistics.add_statistic('mutation_rate',self.mut_prob)
			self.statistics.add_statistic('diversity',self.diversity)
			for statistic in self.extra_statistics:
				print('HERE')
				self.statistics.add_statistic(statistic,self.extra_statistics[statistic](self.fitness_mappings,self))

			result = self.evolution.evolve(self)

			if self.hall_of_fame_injection and (i+1)%20 == 0:
				print('Hall of fame chromosome ',self.hall_of_fame[0] , ' injected to population')
				self.population.new_members.insert(0,self.hall_of_fame[0]) 

			if self.population_control:
				if len(self.population.new_members) > self.population_size:
					self.population.new_members = self.population.new_members[:self.population_size]
				elif len(self.population.new_members) < self.population_size:
					self.population.new_members = self.population.new_members * int(self.population_size/len(self.population.new_members)) + self.population.new_members[:self.population_size%len(self.population.new_members)]
				print('Population Control has taken place')

			if self.efficient_iteration_halt:
				if len(self.last_20_fitnesses)==20:
					self.last_20_fitnesses.popleft()
					self.last_20_fitnesses.append(self.best_fitness[1])
					if all(x == self.last_20_fitnesses[0] for x in self.last_20_fitnesses):
						break
				else:
					self.last_20_fitnesses.append(self.best_fitness[1])

			# For next iteration
			self.population.members = self.population.new_members
			self.population.new_members = []

			if result == 1:
				print('GA Problem Solved')
				break
		print("Best fitness in this generation = ", self.best_fitness)
		print("Best among all generations = ", self.hall_of_fame)
		print("Top fittest chromosomes of this generation: ", self.fitness_mappings[:10])

