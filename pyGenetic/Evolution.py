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
		print(ga.best_fitness[1])
		if ga.best_fitness[1] == ga.fitness_threshold:
			return 1

		p = []
		total = 0
		for chromosome in ga.population.members:
			prob = ga.calculateFitness(chromosome)
			if prob == 0:
				prob = random.uniform(0.01, 0.02)
			total += prob
			p.append(prob)

		p = [ elem/sum(p) for elem in p]
		n = math.ceil(ga.cross_prob * len(p))
		if n %2 == 1:
			n -= 1
			ga.population.members.append(ga.population.members[0])
		#print(p)
		#print(n)
		#print(ga.population.members)	
		#print(p)

		crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)
		#print(crossover_indexes)
		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]
		#print('no of cross',len(crossover_chromosomes))
		for i in range(0,len(crossover_chromosomes)-1,2):
			father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
			c1,c2 = ga.crossover_handlers[0](father,mother)
			ga.population.new_members.extend([c1,c2])
		#print(len(ga.population.new_members))

		#print(len(p))
		mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		#print(mutation_indexes)
		for index in mutation_indexes:
			ga.population.new_members[index] = ga.mutation_handlers[0](ga.population.new_members[index])
		#print(ga.population.new_members)
		ga.population.members = ga.population.new_members
		ga.population.new_members = []  