import random
import copy

class SelectionHandlers:
	@staticmethod
	def basic(pop,fitness_dict,ga):
		pop = sorted(pop,key=lambda x:fitness_dict[1])
		return pop[:int(ga.mut_prob*len(pop))]


class MutationHandlers:
	@staticmethod
	def swap(chromosome):
		index = random.randint(0,len(chromosome)-2)
		newchrom = copy.copy(chromosome)
		newchrom[index], newchrom[index+1] = newchrom[index+1], newchrom[index]
		return newchrom

class CrossoverHandlers:
	@staticmethod
	def distinct(chromosome1,chromosome2):
		# Need to do some error handling here
		r = random.randint(1,len(chromosome1)-2)
		new_chromosome1 = chromosome1[:r]
		for i in chromosome2:
			if i not in new_chromosome1:
				new_chromosome1.append(i)
		new_chromosome2 = chromosome2[:r]
		for i in chromosome1:
			if i not in new_chromosome2:
				new_chromosome2.append(i)
		return new_chromosome1,new_chromosome2

class Fitness:
	@staticmethod
	def sum(chromosome):
		return sum(chromosome)
