import random
import copy
import math

class SelectionHandlers:
	"""
	Class contains staticmethods for selection operation which are
	invoked by  Evolution.py module during selection operation
	
	Methods :
	--------
	basic() : Performs selection operation based fitness scores of candidates

	"""




	@staticmethod
	def basic(pop,fitness_dict,ga):
		"""
		Performs selection operation by selecting the most fittest candidates 
		The number of candidates selected depends on value of cross_prob(crossover probability)

		Parameters :
		-----------
		pop : list
				List containing population of candidates 

		fitness_dict : dictionary
				Contains dictionary of (chromosome : fitness value)

		Returns :
		---------
		List of fittest individuals

		"""

		pop = sorted(pop,key=lambda x:fitness_dict[1])
		return pop[:len(pop)-math.ceil(ga.cross_prob * len(pop))]


class MutationHandlers:
	"""
	Class contains different  mutation handlers to be invoked by Evolution.py
	module during mutation operation 
	
	Methods :
	---------
	swap() : Performs mutation by swapping genes of chromosome in single point manner

	"""

	@staticmethod
	def swap(chromosome):
		"""
		Performs mutation operation on individual chromomsome by random selecting a
		point on chromosome and the exchanging genes from either side of that point 

		Parameters :
		-----------
		chromosome : List

		Returns :
		---------
		Mutated Chromosome

		"""


		index = random.randint(0,len(chromosome)-2)
		newchrom = copy.copy(chromosome)
		newchrom[index], newchrom[index+1] = newchrom[index+1], newchrom[index]
		return newchrom

class CrossoverHandlers:
	"""
	Class contains different static methods to be invoked by Evolution.py module  
	during crossover operation
	
	Method :
	-------

	distinct() : performs crossover between to chromosomes by appending genes from one chromosome 
				into other without duplicating the gene present in first chromosome 

	"""

	@staticmethod
	def distinct(chromosome1,chromosome2):
		"""
		Performs crossover between to chromosomes by appending genes from one chromosome 
		into other without duplicating the gene present in first chromosome

		Parameters :
		------------
		chromosome1 : chromosome as one parent
		chromosome2 : chromosome as second parent

		Returns :
		----------
		Tuple containing two new offspring chromosomes produced by crossover 

		"""

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
	"""
	Class contains staticmethods for calculating fitness score of an individual 

	Methods :
	--------
	sum() : calculates fitness scores of a candidate

	"""

	@staticmethod
	def sum(chromosome):
		"""
		Calculates fitness score of a chromosome as sum of genes

		Parameters :
		-----------
		chromosome : list
		
		Returns :
		----------
		Fitness score 
		"""


		return sum(chromosome)
