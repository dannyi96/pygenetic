import random
from pygenetic import Utils
import math
import numpy as np

class SimpleGA:
	"""
	This Class is the driver program which contains and invokes the operators used in Genetic algorithm
	This class can be invoked to implement a non-generic genetic solution 
	SimpleGA keeps track of specific type of operators the user has specified for running the algorithm

	Methods :
	----------
	create_initial_population() : Generates initial members of population by randomly generating chromosomes based on range
	doCrossover() : Performs crossover by calling specific utility function based on crossover_handler
	doMutation() : Performs mutation by calling specific utility function based on mutation_handler
	calculateFitness() : Returns fitness associated with chromosome passed as argument
	generateFitnessMappings() : Generates a list of population members and associated fitnesses
	handleSelection() : Generates fitness mappings and performs selection by calling specific utility function based on selection_handler
	evolve() : Performs evolution for specified number of iterations

	"""
	def __init__(self,minValue,maxValue,noOfGenes,fitness_func,duplicates=False,population_size=100,cross_prob=0.8,mut_prob=0.1,crossover_handler='onePoint',mutation_handler='swap',selection_handler='best',fitness_type='max'):
		self.minValue = minValue
		self.maxValue = maxValue
		self.noOfGenes = noOfGenes
		self.duplicates = duplicates
		self.population_size = population_size
		self.create_initial_population()
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob
		self.crossover_handler = crossover_handler
		self.mutation_handler = mutation_handler
		self.selection_handler = selection_handler
		self.fitness_type = fitness_type
		if type(self.fitness_type) == str:
			if self.fitness_type == 'max':
				self.best_fitness = None, float("-inf")
			elif self.fitness_type == 'min':
				self.best_fitness = None, float("inf")
		elif type(self.fitness_type) == tuple or type(self.fitness_type) == list:
			if self.fitness_type[0] == 'equal':
				self.best_fitness = None, float("inf")
		self.fitness_func = fitness_func

	def create_initial_population(self):
		"""
		Generates initial members of population by randomly generating chromosomes based on range

		"""
		self.population = []
		for i in range(self.population_size):
			if self.duplicates:
				chromosome = random.choices(range(self.minValue,self.maxValue+1), k = self.noOfGenes)
			else:
				chromosome = random.sample(range(self.minValue,self.maxValue+1), self.noOfGenes)
			self.population.append(chromosome)
		print("Initial population: ", self.population)

	def doCrossover(self, chromosome1, chromosome2):
		"""
		Performs crossover by calling specific utility function based on crossover_handler

		Parameters :
		----------
		chromosome1 : chromosome as one parent
		chromosome2 : chromosome as second parent

		Returns :
		----------
		Tuple containing two new offspring chromosomes produced by crossover 

		"""
		if self.crossover_handler == 'distinct':
			return Utils.CrossoverHandlers.distinct(chromosome1,chromosome2)
		elif self.crossover_handler == 'onePoint':
			return Utils.CrossoverHandlers.onePoint(chromosome1,chromosome2)
		elif self.crossover_handler == 'twoPoint':
			return Utils.CrossoverHandlers.twoPoint(chromosome1,chromosome2)
		elif self.crossover_handler == 'PMX':
			return Utils.CrossoverHandlers.PMX(chromosome1,chromosome2)
		elif self.crossover_handler == 'OX':
			return Utils.CrossoverHandlers.OX(chromosome1,chromosome2)
		else:
			raise Exception('Invalid Crossover given as input')

	def doMutation(self, chromosome1):
		"""
		Performs mutation by calling specific utility function based on mutation_handler

		Parameters :
		----------
		chromosome1 : chromosome as subject

		Returns :
		----------
		Mutated chromosome

		"""
		if self.mutation_handler == 'swap':
			return Utils.MutationHandlers.swap(chromosome1)
		elif self.mutation_handler == 'bitFlip':
			return Utils.MutationHandlers.bitFlip(chromosome1)
		else:
			raise Exception('Invalid Mutation given as input')

	def calculateFitness(self,chromosome):
		"""
		Returns fitness associated with chromosome passed as argument

		Parameters :
		----------
		chromosome : chromosome whose fitness is to be calculated

		Returns :
		----------
		Fitness of that chromosome

		"""
		return self.fitness_func(chromosome)

	def generateFitnessMappings(self):
		"""
		Generates a list of population members and associated fitnesses

		"""
		self.fitness_mappings = [(member, self.calculateFitness(member)) for member in self.population]
		print(self.fitness_mappings)	

	def handle_selection(self):
		"""
		Generates fitness mappings and performs selection by calling specific utility function based on selection_handler

		Returns :
		----------
		Filtered population list based on selection method

		"""
		self.generateFitnessMappings()
		if self.fitness_type == 'max':
			self.fitness_mappings.sort(key=lambda x:x[1],reverse=True)
			self.best_fitness = self.fitness_mappings[0]
		elif self.fitness_type == 'min':
			self.fitness_mappings.sort(key=lambda x:x[1])
			self.best_fitness = self.fitness_mappings[0]
		elif self.fitness_type[0] == 'equal':
			self.fitness_mappings.sort(key=lambda x:abs(x[1]-self.fitness_type[1]))
			self.best_fitness = self.fitness_mappings[0]
		else:
			raise Exception('Invalid fitness type')

		if self.selection_handler == 'best':
			return Utils.SelectionHandlers.best(self.fitness_mappings,self)
		elif self.selection_handler == 'roulette':
			return Utils.SelectionHandlers.roulette(self.fitness_mappings,self)
		elif self.selection_handler == 'rank':
			return Utils.SelectionHandlers.rank(self.fitness_mappings,self)
		else:
			raise Exception('Invalid Mutation given as input')

	def evolve(self,noOfIterations=50):
		"""
		Performs the evolution as many times as number of iterations specified by user or terminates
		if optimal solution is found.

		Parameters :
		-----------
		noOfIterations : int
						default value : 50

		Outline of Algorithm :
		---------------------
		Selection : fittest members of population are selected by invoking 
					selection handler in Utils.py module
		Crossover : A probability score is generated from fitness value of each chromosome
					Chromosomes for crossover are selected based on this probablity score 
					of each chromosome
					Crossover is performed by invoking a crossover handler from Utils.py
		Mutation : The genes to be mutated are chosen randomly
					Once indexes of Chromomsome / genes to be mutated are determined, a mutation
					handler from Utils.py module is invoked 

		Each iteration consists of repeating the above operations until an optimal solution 
		determined by fitness threshold is reached  or number of iterations specified are complete

		"""
		for i in range(noOfIterations):
			new_population = self.handle_selection()
			print("*** Members left after selection = ",len(new_population))
			print("Best member = ",self.best_fitness[0])
			print("Best fitness = ",self.best_fitness[1])
			if self.fitness_type[0] == 'equal':
				if self.best_fitness[1] == self.fitness_type[1]:
					print('Solved')
					return 1
			fitnesses = []
			total = 0
			for chromosome in self.fitness_mappings:
				fitness = chromosome[1]
				if fitness == 0:
					fitness = random.uniform(0.01, 0.02)
				total += fitness
				fitnesses.append(fitness)
			print(fitnesses)	
			p = [ elem/total for elem in fitnesses]
			n = math.ceil(self.cross_prob * len(p))
			if n %2 == 1:
				n -= 1
				self.population.append(self.population[0])

			crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)

			crossover_chromosomes = [ self.population[index] for index in crossover_indexes]

			for i in range(0,len(crossover_chromosomes)-1,2):
				father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
				child1, child2 = self.doCrossover(father,mother)
				new_population.extend([child1,child2])
			mutation_indexes = np.random.choice(len(new_population),int(self.mut_prob*len(p)), replace=False)
			for index in mutation_indexes:
				new_population[index] = self.doMutation(new_population[index])
			self.population = new_population
			new_population = []
		print("Best fitness in this generation = ", self.best_fitness)
		print("Top 10 fitnesses in this generation = ", self.fitness_mappings[:10])
