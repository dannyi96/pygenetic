from abc import ABC, abstractmethod
import random
import math
import numpy as np

class BaseEvolution(ABC):

	def __init__(self,max_iterations):
		self.max_iterations = max_iterations

	@abstractmethod
	def evolve(self,ga):
		pass

class StandardEvolution(BaseEvolution):

	def __init__(self,max_iterations=100):
		BaseEvolution.__init__(self,max_iterations)

	def evolve(self,ga):
		#print(self.max_iterations)
		# get (1-r) * cross_prob new members
		ga.population.new_members = ga.handle_selection()
		#print(len(ga.population.members))
		#print(ga.population.new_members)
		#print(ga.highest_fitness[1])
		if ga.highest_fitness[1] == ga.fitness_threshold:
			return 1
		total = 0
		for chromosome in ga.population.members:
			total += ga.calculateFitness(chromosome)
		p = [ ga.calculateFitness(chromosome)/total for chromosome in ga.population.members]
		n = math.ceil(ga.cross_prob * len(p)) 
		if n %2 == 1:
			n -= 1
		#print(p)
		#print(n)
		#print(ga.population.members)
		crossover_indexes = np.random.choice(len(p),n,p)
		#print(crossover_indexes)
		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]

		for i in range(0,len(crossover_chromosomes)-2,2):
			father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
			c1,c2 = ga.crossover_handlers[0](father,mother)
			ga.population.new_members.extend([c1,c2])
		print(ga.population.new_members)
		mutation_indexes = np.random.choice(len(p),int(ga.mut_prob*len(p)),p)
		print(mutation_indexes)
		for index in mutation_indexes:
			ga.population.new_members[index] = ga.mutation_handlers[0](ga.population.new_members[index])
		print(ga.population.new_members)
		ga.population.members = ga.population.new_members
		ga.population.new_members = []  