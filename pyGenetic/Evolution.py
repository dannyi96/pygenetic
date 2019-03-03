from abc import ABC, abstractmethod
import random

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
		print(self.max_iterations)
		ga.population.new_members = ga.handle_selection()
		print(ga.population.new_members)
		print(ga.highest_fitness[1])
		if ga.highest_fitness[1] == ga.fitness_threshold:
			return 1
		iteration_size = len(ga.population.new_members)
		if iteration_size%2==1:
			iteration_size -= 1
		for i in range(0,iteration_size,2):
			father, mother = ga.population.new_members[i], ga.population.new_members[i+1]
			if random.random() <= ga.cross_prob:
				child1, child2 = ga.crossover_handlers[0](father,mother)
				ga.population.new_members.append(child1)
				ga.population.new_members.append(child2)
			if random.random() <= ga.mut_prob:
				child = ga.mutation_handlers[0](father)
				ga.population.new_members.append(child)
			if random.random() <= ga.mut_prob:
				child = ga.mutation_handlers[0](mother)
				ga.population.new_members.append(child) 