import random
import copy
import math
import operator

class SelectionHandlers:
	@staticmethod
	def basic(pop,fitness_dict,ga):
		pop = sorted(pop,key=lambda x:fitness_dict[1])
		return pop[:len(pop)-math.ceil(ga.cross_prob * len(pop))]

	@staticmethod
	def random(pop, fitness_dict, ga):
		return [random.choice(pop) for i in range(ga.population.population_size)]

	@staticmethod
	def worst(pop, fitness_dict, ga):
		new = sorted(fitness_dict, key=operator.itemgetter(1))[:ga.population.population_size]
		return [i[0] for i in new]
		
	@staticmethod
	def best(pop, fitness_dict, ga):
		new = sorted(fitness_dict, key=operator.itemgetter(1), reverse=True)[:ga.population.population_size]
		return [i[0] for i in new]
		
	@staticmethod
	def tournament(pop, fitness_dict, ga):
		# tournsize is by default defined as 3
		chosen = []
		for i in range(ga.population.population_size):
			aspirants = random.sample(fitness_dict,ga.tournsize)
			chosen.append(max(aspirants, key=operator.itemgetter(1)))
		return [i[0] for i in chosen]
		
	@staticmethod
	def roulette(pop, fitness_dict, ga):
		fitness = [i[1] for i in fitness_dict]
		total_fit = float(sum(fitness))
		relative_fitness = [f/total_fit for f in fitness]
		probabilities = [sum(relative_fitness[:i+1]) for i in range(len(relative_fitness))]
		chosen = []
		for n in range(ga.population.population_size):
			r = random.random()
			for (i, individual) in enumerate(pop):
				if r <= probabilities[i]:
					chosen.append(list(individual))
					break
		return chosen

	@staticmethod
	def rank(pop, fitness_dict, ga):
		new = [i[0] for i in sorted(fitness_dict, key=operator.itemgetter(1))]
		for i in range(len(new)):
			new[i]=(new[i],i+1)
		return SelectionHandlers.roulette(pop, new, ga)

	@staticmethod
	def SUS(pop, fitness_dict, ga):
		s_inds = sorted(fitness_dict, key=operator.itemgetter(1), reverse=True)
		distance = sum([i[1] for i in fitness_dict]) / float(ga.population.population_size)
		start = random.uniform(0, distance)
		points = [start + i*distance for i in range(ga.population.population_size)]
		chosen = []
		for p in points:
			i = 0
			sum_ = s_inds[i][1]
			while sum_ < p:
				i += 1
				sum_ += s_inds[i][1]
			chosen.append(s_inds[i][0])
		return chosen


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
	def addition(chromosome):
		return sum(chromosome)
		
	@staticmethod
	def TSP(chromosome, matrix):
		total = 0
		for i in range(len(chromosome)-1):
			total += matrix[chromosome[i]][chromosome[i+1]]
		return total
