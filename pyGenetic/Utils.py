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

	# only when genes are binary
	@staticmethod
	def bitFlip(chromosome):
		index = random.randint(0,len(chromosome))
		chromosome[index] = type(chromosome[index])(not chromosome[index])
		return chromosome

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
		
	@staticmethod
	def onePoint(chromosome1, chromosome2):
		size = min(len(chromosome1), len(chromosome2))
		r = random.randint(1, size - 1)
		new_chromosome1 = chromosome1[:r]+chromosome2[r:]
		new_chromosome2 = chromosome2[:r]+chromosome1[r:]
		return new_chromosome1, new_chromosome2

	@staticmethod
	def twoPoint(chromosome1, chromosome2):
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = chromosome1[:a]+chromosome2[a:b]+chromosome1[b:]
		new_chromosome2 = chromosome2[:a]+chromosome1[a:b]+chromosome2[b:]
		return new_chromosome1, new_chromosome2
		
	@staticmethod
	def PMX(chromosome1, chromosome2): # Partially Matched Crossover
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = chromosome1[:a]+chromosome2[a:b]+chromosome1[b:]
		new_chromosome2 = chromosome2[:a]+chromosome1[a:b]+chromosome2[b:]
		mapping1=chromosome2[a:b]
		mapping2=chromosome1[a:b]
		i = b
		while(i!=a):
			while new_chromosome1[i] in mapping1:
				new_chromosome1[i] = mapping2[mapping1.index(new_chromosome1[i])]
			while new_chromosome2[i] in mapping2:
				new_chromosome2[i] = mapping1[mapping2.index(new_chromosome2[i])]
			i = (i+1)%size
		return new_chromosome1, new_chromosome2
	
	@staticmethod
	def OX(chromosome1, chromosome2): # Ordered Crossover
		size = min(len(chromosome1), len(chromosome2))
		a = random.randint(1, size - 2)
		b = random.randint(1, size - 1)
		if b==a:
			b+=1
		elif b<a:
			a,b=b,a
		new_chromosome1 = [None]*(a)+chromosome1[a:b]+[None]*(size-b)
		new_chromosome2 = [None]*(a)+chromosome2[a:b]+[None]*(size-b)
		i,j,k = b,b,b
		while True:
			if chromosome2[i] not in new_chromosome1:
				new_chromosome1[j] = chromosome2[i]
				j = (j+1)%size
			if chromosome1[i] not in new_chromosome2:
				new_chromosome2[k] = chromosome1[i]
				k = (k+1)%size
			i = (i+1)%size
			if i==b or (j==a and k==a):
				break
		return new_chromosome1, new_chromosome2


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
