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


	def __init__(self,factory,population_size=100,cross_prob=0.8,mut_prob=0.1,fitness_type='max',adaptive_mutation=True, use_pyspark=False):
		self.fitness_func = None
		self.factory = factory
		self.population = Population.Population(factory,population_size)
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob
		self.adaptive_mutation = adaptive_mutation
		self.crossover_handlers = []
		self.crossover_handlers_weights = []
		self.mutation_handlers = []
		self.mutation_handlers_weights = []
		self.selection_handler = None
		self.fitness_type = fitness_type
		if type(self.fitness_type) == str:
			if self.fitness_type == 'max':
				self.best_fitness = None, float("-inf")
			elif self.fitness_type == 'min':
				self.best_fitness = None, float("inf")
		elif type(self.fitness_type) == tuple or type(self.fitness_type) == list:
			if self.fitness_type[0] == 'equal':
				self.best_fitness = None, float("inf")
		if adaptive_mutation == True:
			self.dynamic_mutation = None
			self.diversity = None
		self.statistics = Statistics.Statistics()
		self.evolution = Evolution.StandardEvolution(adaptive_mutation=adaptive_mutation,pyspark=use_pyspark)
		self.fitness_external_data = []

	def addCrossoverHandler(self,crossover_handler, weight = 1):
		"""
		Adds crossover handler staticmethod defined in Utils.py and
		appends the weightage to be given to the handler

		Parameters :
		----------
		crossover_handler : Method defined in Utils.py
		weight : int

		"""

		#try: 
		#	crossoverhandlers = dir(Utils.CrossoverHandlers)
		#	if crossover_handler not in crossoverhandlers:
		#		raise NotImplementedError('No such crossover handler found')


		self.crossover_handlers.append(crossover_handler)
		self.crossover_handlers_weights.append(weight)
		
		#except NotImplementedError as ni:
		#	print(ni)

			

	def addMutationHandler(self,mutation_handler, weight = 1):
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

	def setCrossoverProbability(self,cross_prob):
		"""
		Sets crossover probability value

		Parameters :
		-----------
		cross_prob : float

		"""

		self.cross_prob = cross_prob

	def setMutationProbability(self,mut_prob):
		"""
		Sets mutation probability instance variable

		Parameters:
		----------
		Mutation probability

		"""
		self.mut_prob = mut_prob

	def setSelectionHandler(self,selection_handler):
		"""
		Sets function to be used for selection_handler

		Parameters:
		----------
		Function to be used for selection_handler

		"""
		self.selection_handler = selection_handler

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

	def generateFitnessDict(self):
		"""
		Generates a  dictionary of (individual, fitness_score) and also stores the dictionary
		containing fittest chromosome depending on fitness_type(max/min/equal)

		"""

		self.fitness_dict = [(member, self.calculateFitness(member)) for member in self.population.members]
		if self.fitness_type == 'max':
			self.fitness_dict.sort(key=lambda x:x[1],reverse=True)
		elif self.fitness_type == 'min':
			self.fitness_dict.sort(key=lambda x:x[1])
		elif self.fitness_type[0] == 'equal':
			self.fitness_dict.sort(key=lambda x:abs(x[1]-self.fitness_type[1]))
		self.best_fitness = self.fitness_dict[0]

	def handle_selection(self):

		"""
		Invokes generateFitnessDict() to generate dictionary of (chromosome,fitness)
		Invokes selection_handler staticmethod defined in Utils.py module

		Returns :
		---------
		List of  fittest members of population

		"""
		self.generateFitnessDict()
		return self.selection_handler(self.population.members,self.fitness_dict,self)

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

		self.normalizeWeights()
		for i in range(noOfIterations):
			result = self.evolution.evolve(self)
			self.statistics.add_statistic('best',self.fitness_dict[0][1])
			self.statistics.add_statistic('worst',self.fitness_dict[-1][1])
			print('Fitness Dict', self.fitness_dict)
			fitnesses = [x[1] for x in self.fitness_dict]
			self.statistics.add_statistic('avg',sum(fitnesses)/len(fitnesses))
			if self.adaptive_mutation:
				self.statistics.add_statistic('mutation_rate',self.dynamic_mutation)
				self.statistics.add_statistic('diversity',self.diversity)
			if result:
				print('SOLVED')
				break
		print(self.fitness_dict[:10])

	def continue_evolve(self, noOfIterations=20):
		self.normalizeWeights()
		for i in range(noOfIterations):
			result = self.evolution.evolve(self)
			self.statistics.add_statistic('best',self.fitness_dict[0][1])
			self.statistics.add_statistic('worst',self.fitness_dict[-1][1])
			print('Fitness Dict', self.fitness_dict)
			fitnesses = [x[1] for x in self.fitness_dict]
			self.statistics.add_statistic('avg',sum(fitnesses)/len(fitnesses))
			if self.adaptive_mutation:
				self.statistics.add_statistic('mutation_rate',self.dynamic_mutation)
				self.statistics.add_statistic('diversity',self.diversity)
			if result:
				print('SOLVED')
				break
		#self.statistics.plot_statistics(['max','min','avg'])
		#if self.adaptive_mutation:
		#	self.statistics.plot_statistics(['diversity','mutation_rate'])


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


	ga = GAEngine(factory,100,fitness_type='min',mut_prob = 0.3)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)

	#ga = GAEngine(fitness,8,factory,20)#,fitness_type='equal')
	#ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 9)

	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
	ga.addMutationHandler(Utils.MutationHandlers.swap)

	ga.setSelectionHandler(Utils.SelectionHandlers.SUS)
	ga.setFitnessHandler(Utils.Fitness.TSP, matrix)
	# ga.setSelectionHandler(Utils.SelectionHandlers.basic)
	# Provide max iteration here ???
	ga.evolve(20)
