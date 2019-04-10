import Population
import ChromosomeFactory
import random
import numpy as np
import collections
import Utils
import Evolution
import Statistics
import bisect
import math

class SimpleGA:

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
		self.population = []
		for i in range(self.population_size):
			if self.duplicates:
				chromosome = random.choices(range(self.minValue,self.maxValue+1), k = self.noOfGenes)
			else:
				chromosome = random.sample(range(self.minValue,self.maxValue+1), self.noOfGenes)
			self.population.append(chromosome)
		#print(self.population)

	def doCrossover(self, chromosome1, chromosome2):
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
		if self.mutation_handler == 'swap':
			return Utils.MutationHandlers.swap(chromosome1)
		elif self.crossover_handler == 'bitFlip':
			return Utils.MutationHandlers.bitFlip(chromosome1)
		else:
			raise Exception('Invalid Mutation given as input')

	def calculateFitness(self,chromosome):
		return self.fitness_func(chromosome)

	def generateFitnessDict(self):
		self.fitness_dict = [(member, self.calculateFitness(member)) for member in self.population]
		print(self.fitness_dict)	

	def handle_selection(self):
		self.generateFitnessDict()
		if self.fitness_type == 'max':
			self.fitness_dict.sort(key=lambda x:x[1],reverse=True)
			self.best_fitness = self.fitness_dict[0]
		elif self.fitness_type == 'min':
			self.fitness_dict.sort(key=lambda x:x[1])
			self.best_fitness = self.fitness_dict[0]
		elif self.fitness_type[0] == 'equal':
			self.fitness_dict.sort(key=lambda x:abs(x[1]-self.fitness_type[1]))
			self.best_fitness = self.fitness_dict[0]
		else:
			raise Exception('Invalid fitness type')

		if self.selection_handler == 'best':
			return Utils.SelectionHandlers.best(self.population,self.fitness_dict,self)
		elif self.selection_handler == 'roulette':
			return Utils.SelectionHandlers.roulette(self.population,self.fitness_dict,self)
		elif self.selection_handler == 'rank':
			return Utils.SelectionHandlers.rank(self.population,self.fitness_dict,self)
		else:
			raise Exception('Invalid Mutation given as input')

	def evolve(self,noOfIterations=50):
		for i in range(noOfIterations):
			new_population = self.handle_selection()
			print("*** Members left after selection = ",len(new_population))
			print("Best member = ",ga.best_fitness[0])
			print("Best fitness = ",ga.best_fitness[1])
			if ga.fitness_type[0] == 'equal':
				if ga.best_fitness[1] == ga.fitness_type[1]:
					print('Solved')
					return 1
			fitnesses = []
			total = 0 #This is not being used
			for chromosome in ga.fitness_dict:
				fitness = chromosome[1]
				if fitness == 0:
					fitness = random.uniform(0.01, 0.02)
				total += fitness
				fitnesses.append(fitness)
			print(fitnesses)	
			p = [ elem/total for elem in fitnesses]
			n = math.ceil(ga.cross_prob * len(p))
			if n %2 == 1:
				n -= 1
				self.population.append(self.population[0])

			crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)
			#print("crossover_indices = ",crossover_indexes)

			crossover_chromosomes = [ self.population[index] for index in crossover_indexes]

			for i in range(0,len(crossover_chromosomes)-1,2):
				father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
				child1, child2 = ga.doCrossover(father,mother)
				new_population.extend([child1,child2])
			#print("adaptive_mutation value passed = ",self.adaptive_mutation)
			mutation_indexes = np.random.choice(len(new_population),int(ga.mut_prob*len(p)), replace=False)
			for index in mutation_indexes:
				new_population[index] = ga.doMutation(new_population[index])
			self.population = new_population
			#print("New members = ",ga.population.members)
			new_population = []
		print("Best fitness in this generation = ", self.best_fitness)
		print(self.fitness_dict[:10])
	
if __name__ == '__main__':
	ga = SimpleGA(minValue=1,maxValue=10,noOfGenes=10,fitness_func=lambda x:sum(x),duplicates=False,population_size=100,cross_prob=0.8,mut_prob=0.1,crossover_handler='onePoint',mutation_handler='swap',selection_handler='best',fitness_type='max')
	ga.generateFitnessDict()
	ga.evolve(2)