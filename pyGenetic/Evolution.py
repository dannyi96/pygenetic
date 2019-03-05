from abc import ABC, abstractmethod
import random
import math
import numpy as np
#import pyspark

class BaseEvolution(ABC):

	def __init__(self,max_iterations):
		self.max_iterations = max_iterations

	@abstractmethod
	def evolve(self,ga):
		pass

class StandardEvolution(BaseEvolution):

	def __init__(self,max_iterations=100,adaptive_mutation=True,pyspark=False):
		BaseEvolution.__init__(self,max_iterations)
		self.adaptive_mutation = adaptive_mutation
		self.pyspark = pyspark

	def __evolve_normal(self,ga):
		# get (1-r) * cross_prob new members
		ga.population.new_members = ga.handle_selection()

		print(ga.best_fitness[1])
		if ga.best_fitness[1] == ga.fitness_threshold:
			return 1

		fitnesses = []
		total = 0
		for chromosome in ga.population.members:
			fitness = ga.calculateFitness(chromosome)
			if fitnesses == 0:
				fitness = random.uniform(0.01, 0.02)
			total += fitness
			fitnesses.append(fitness)

		p = [ elem/sum(fitnesses) for elem in fitnesses]
		n = math.ceil(ga.cross_prob * len(p))
		if n %2 == 1:
			n -= 1
			ga.population.members.append(ga.population.members[0])

		crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)

		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]

		for i in range(0,len(crossover_chromosomes)-1,2):
			father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
			child1, child2 = ga.crossover_handlers[0](father,mother)
			ga.population.new_members.extend([child1,child2])
		print(self.adaptive_mutation)
		if self.adaptive_mutation == True:
			mean_fitness = sum(fitnesses)/len(fitnesses)
			average_square_deviation = math.sqrt(sum((fitness - mean_fitness)**2 for fitness in fitnesses)) / len(fitnesses)
			ga.dynamic_mutation = ga.mut_prob * ( 1 + ( (ga.best_fitness[1]-average_square_deviation) / (ga.best_fitness[1]+average_square_deviation) ) )
			print('Adaptive mutation ',ga.dynamic_mutation)
			mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.dynamic_mutation*len(p)), replace=False)
		else:
			mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		for index in mutation_indexes:
			ga.population.new_members[index] = ga.mutation_handlers[0](ga.population.new_members[index])
		ga.population.members = ga.population.new_members
		ga.population.new_members = []  



	#def __evolve_pyspark(self,ga):


	def evolve(self,ga):
		#print(self.max_iterations)
		if self.pyspark == False:
			if self.__evolve_normal(ga):
				return 1



