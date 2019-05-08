from pygenetic import Population, Evolution, Statistics
import random
import collections
import bisect
import math
import numpy as np

class GAEngine:
	"""
	This Class is the main driver program which contains and invokes the operators used in Genetic algorithm

	GAEngine keeps track of specific type of operators the user has specified for running the algorithm

	Methods :
	---------
	addCrossoverHandler(crossover_handler, weight, *args)
		Sets the function to be used for crossover operation

	addMutationHandler(mutation_handler, weight, *args)
		Sets the function to be used for mutation operation

	doCrossover(cross_func, member1, member2)
		Calls crossover handler passing 2 given members as parameters

	doMutation(self, mut_func, member)
		Calls mutation handler passing member as parameter

	setSelectionHandler(selection_handler, *args)
		Sets the function to be used for selection operation

	setFitnessHandler(fit_function, *args)
		Sets the function to be used for calculating fitness of chromosome

	calculateFitness(chromosome)
		Invokes fitness function (fitness_func) to compute the fitness score of a chromosome

	generateFitnessMappings()
		Generates a list of tuples (individual, fitness_score) and also stores the tuple
		containing fittest chromosome [best_fitness] depending on fitness_type(max/min/equal)

	handle_selection(repeat_chromosome_sorting=False)
		Invokes generateFitnessMappings() if repeat_chromosome_sorting=True and  selection_handler called

	normalizeWeights()
		Normalizes crossover and mutation handler weights, result is a CDF

	chooseCrossoverHandler()
		Selects crossover handler from available handlers based on weightage given to handlers

	chooseMutationHandler()
		Selects mutation handler from available handlers based on weightage given to handlers

	setEvolution(evolution)
		Sets evolution instance member to the parameter passed during class initialization

	addStatistic(statistic,statistic_function)
		Appends a new statistic function

	evolve(noOfIterations=50)
		The interface provided to start evolution

	continue_evolve(noOfIterations=20)
		Performs the evolution by invoking the evolve method from Evolution.py module
		as many times as number of iterations specified by user or terminates if optimal
		solution is found.
		Also invokes compute method from Statistics.py module to generate graph


	Instance Members
	-----------
	fitness_func : A function reference
				The fitness function to be used, passed as a function argument

	factory : Instance of any subclass of ChromosomeFactory class
				Generates and returns the initial population of candidate solutions

	population_size : int
				The number of candidate solutions that can exist after every iteration

	cross_prob : float (0.0 to 1.0)
				The Crossover probability of crossover operation which determines the extent to which crossover between parents
				(default is 0.7)

	mut_prob : float (0.0 to 1.0)
				The mutation probability of mutation operation which determines extent to which candidates should be mutated
				(default is 0.1)

	fitness_type : string
				Indicates the nature of fitness value (higher/lower/equal) to be considered during selection of candidates
				(default is max)

	adaptive_mutation : boolean
				If set rate of mutation of candidates dynamically changes during execution depending on diversity in population
				(default is true)

	initial_mut_prob : float
				If adaptive mutation is True, this stores the initial mutation probability

	crossover_handlers : list
				Stores all crossover handlers added to solve problem

	crossover_handlers_weights : list
				Stores the weights associated with crossover handlers in crossover_handlers. Sums up to 1

	mutation_handlers : list
				Stores all mutation handlers added to solve problem

	mutation_handlers_weights : list
				Stores the weights associated with mutation handlers in mutation_handlers. Sums up to 1

	selection_handler : A function reference
				Stores the function selected by user to perform selection

	fitness_mappings : list
				List containing population and associated fitness values, refreshed each generation

	population : Class Instance
				An instance of the class "Population" used to create initial population.

	best_fitness : tuple
				Stores the best fitness for each generation

	evolution : Class Instance
				An instance of any class that supports implementation of evolution

	population_control : boolean
				If true, population size is maintained. Else, population size may vary in each iteration

	hall_of_fame_injection : boolean
				If true, best chromosome among all past generations is injected into population after a set number of generations

	efficient_iteration_halt : boolean
				If true, halts evolution when the best chromosome remains the same for a consecutive number of generations

	fitness_external_data : list
				Stores any additional data structures required for fitness calculation

	selection_external_data : list
				Stores any additional data structures required to perform selection

	crossover_external_data : dict
				Stores any additional data required to perform crossover. Data is mapped to specific crossover function

	mutation_external_data : dict
				Stores any additional data required to perform mutation. Data is mapped to specific mutation function

	hall_of_fame : tuple
				Stores the best chromosome among all the chromosomes generated in all past generations

	extra_statistics : dict
				Stores any extra statistics added by user

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
		crossover_handler : Method defined in Utils.py or custom
		weight : integer relative weightage
		any number of extra data required for specific handler

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
		mutation_handler : Method defined in Utils.py or custom
		weight : integer relative weightage
		any number of extra data required for specific handler

		"""

		self.mutation_handlers.append(mutation_handler)
		self.mutation_handlers_weights.append(weight)
		xtra_args = []
		for arg in args:
			xtra_args.append(arg)
		self.mutation_external_data.update({mutation_handler:tuple(xtra_args)})

	def doCrossover(self, cross_func, member1, member2):
		"""
		Calls crossover handler passing 2 given members as parameters

		Parameters :
		----------
		cross_func : Crossover handler to be used
		member1 : Parent 1
		member2 : Parent 2

		Returns :
		----------
		Tuple containing two children chromosomes resulting from crossover between passed parents
		"""
		if cross_func in self.crossover_external_data:
			return cross_func(member1, member2, *(self.crossover_external_data[cross_func]))
		else:
			return cross_func(member1, member2)

	def doMutation(self, mut_func, member):
		"""
		Calls mutation handler passing a member as parameter

		Parameters :
		----------
		mut_func : mutation handler to be used
		member : The chromosome to perform mutation on

		Returns :
		----------
		A chromosome resulting from mutation on passed member
		"""
		if mut_func in self.mutation_external_data:
			return mut_func(member, *(self.mutation_external_data[mut_func]))
		else:
			return mut_func(member)

	def setSelectionHandler(self,selection_handler, *args):
		"""
		Sets function to be used for selection_handler

		Parameters:
		----------
		selection_handler : Function to be used to perform selection, can be custom
		any extra data required to do selection 

		"""
		self.selection_handler = selection_handler
		for arg in args:
			self.selection_external_data.append(arg)

	def setFitnessHandler(self, fit_function, *args):
		"""
		Sets function to be used to calculate fitness

		Parameters:
		----------
		fit_function : Function to be used to calculate fitness of a chromosome, can be custom
		any extra data required to calculate fitness 

		"""
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
		Generates a list of tuples (individual, fitness_score) and also stores the tuple
		containing fittest chromosome [best_fitness] depending on fitness_type(max/min/equal)

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
		Invokes generateFitnessMappings() if repeat_chromosome_sorting=True to generate list of (chromosome,fitness)
		Invokes selection_handler staticmethod defined in Utils.py module or custom

		Parameters :
		----------
		repeat_chromosome_sorting : To sort before selection or not

		Returns :
		---------
		List of limited number of fittest members of population

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
		total = sum(self.crossover_handlers_weights)
		cumsum = 0
		for i in range(len(self.crossover_handlers_weights)):
			cumsum += self.crossover_handlers_weights[i]
			self.crossover_handlers_weights[i] = cumsum/total

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
		"""
		Sets evolution instance member to the parameter passed during class initialization

		Parameters :
		----------
		evolution : A predefined evoluton class instance or instance of custom class

		"""
		self.evolution = evolution

	def addStatistic(self,statistic,statistic_function):
		"""
		Appends a new statistic function

		Parameters :
		----------
		statistic : The statistic for which to add the function being passed
		statistic_function : The function to be added to the statistic

		"""
		if type(statistic) != str:
			raise Exception('Invalid Statistics key')
		self.extra_statistics[statistic] = statistic_function

	def evolve(self,noOfIterations=50):
		"""
		The interface provided to start evolution

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
		"""
		Performs the evolution by invoking the evolve method from Evolution.py module
		as many times as number of iterations specified by user or terminates if optimal
		solution is found.
		Also invokes compute method from Statistics.py module to generate graph

		Parameters :
		-----------
		noOfIterations : int
						default value : 20

		"""
		self.normalizeWeights()
		if self.population == None:
			raise Exception('Call evolve before calling continue_evolve')
		print("gen\tavg\t\tbest\tworst\t")
		i=0
		while i<noOfIterations:
			self.generateFitnessMappings()
			fitnesses = [ x[1] for x in self.fitness_mappings]
			self.statistics.add_statistic('best-fitness',self.fitness_mappings[0][1])
			self.statistics.add_statistic('worst-fitness',self.fitness_mappings[-1][1])
			self.mean_fitness = sum(fitnesses)/len(fitnesses)
			self.statistics.add_statistic('avg-fitness',self.mean_fitness)
			self.diversity = math.sqrt(sum((fitness - self.mean_fitness)**2 for fitness in fitnesses)) / len(fitnesses)
			print("%i\t%.2f\t\t%s\t%s\t" % (len(self.statistics.statistic_dict['best-fitness']),self.mean_fitness,self.fitness_mappings[0][1],self.fitness_mappings[-1][1]))
			if self.adaptive_mutation:
				self.mut_prob = self.initial_mut_prob * ( 1 + ((self.best_fitness[1]-self.diversity) / (self.diversity+self.best_fitness[1]) ) )
				self.mut_prob = np.clip(self.mut_prob,0.0001,0.8)
			self.statistics.add_statistic('mutation_rate',self.mut_prob)
			self.statistics.add_statistic('diversity',self.diversity)
			for statistic in self.extra_statistics:
				self.statistics.add_statistic(statistic,self.extra_statistics[statistic](self.fitness_mappings,self))

			result = self.evolution.evolve(self)

			if self.hall_of_fame_injection and (i+1)%20 == 0:
				self.population.new_members.insert(0,self.hall_of_fame[0]) 

			if self.population_control:
				if len(self.population.new_members) > self.population_size:
					self.population.new_members = self.population.new_members[:self.population_size]
				elif len(self.population.new_members) < self.population_size:
					self.population.new_members = self.population.new_members * int(self.population_size/len(self.population.new_members)) + self.population.new_members[:self.population_size%len(self.population.new_members)]

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
			i += 1

