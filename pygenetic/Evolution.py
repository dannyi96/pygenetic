from abc import ABC, abstractmethod
import random
import math
from pygenetic import Utils
# import Utils
import numpy as np

class BaseEvolution(ABC):
	"""
	Abstract class to be inherited to implement the specific evolution procedure

	Methods :
	---------
	evolve() : abstract method to be implemeted by derived classes

	"""

	def __init__(self):
		pass

	@abstractmethod
	def evolve(self,ga):
		"""
		Abstract method to be implemeted by derived classes
		
		Parameters :
		-------------
		ga : reference to the GAEngine object

		"""

		pass

class StandardEvolution(BaseEvolution):
	"""
	Class inherits from BaseEvolution and contains implementations of abstract 
	evolution method in BaseEvolution

	Instance Members :
	------------------

	pyspark : boolean to indicated if parallelization should be supported by using pyspark

	"""
	def __init__(self,pyspark=False):
		self.pyspark = pyspark

	def __evolve_normal(self,ga):

		"""
		Private method which performs an iteration

		Parameters :
		-------------
		ga : reference to the GAEngine object

		Outline of Algorithm :
		---------------------
		Selection : fittest members of population are selected by invoking 
					selection handler in Utils.py module
		Crossover : A probability score is generated from fitness value of each chromosome
					Chromosomes for crossover are selected based on this probablity score 
					of each chromosome
					Crossover is performed by invoking a crossover handler from Utils.py
		Mutation : If adaptive mutation is set then average square deviation of fitness values
					is used for determining (the indexes of chromosome)/genes to be mutated 
					If false then genes to be mutated are chosen randomly
					Once indexes of Chromomsome / genes to be mutated are determined, a mutation
					handler from Utils.py module is invoked 

		Each iteration consists of repeating the above operations until an optimal solution 
		determined by fitness threshold is reached  or number of iterations specified are complete

		"""

		# get (1-r) * cross_prob new members
		ga.population.new_members = ga.handle_selection()
		# print("Members left after selection = ",len(ga.population.members))
		# print("Best member after selection = ",ga.best_fitness[0])
		# print("Best fitness after selection = ",ga.best_fitness[1])
		if ga.fitness_type[0] == 'equal':
			if ga.best_fitness[1] == ga.fitness_type[1]:
				return 1

		fitnesses = []
		total_fitness = 0
		for chromosome in ga.fitness_mappings:
			fitness = chromosome[1]
			if fitness <= 0:
				fitness = random.uniform(0.01, 0.02)
			total_fitness += fitness
			fitnesses.append(fitness)

		p = [ elem/total_fitness for elem in fitnesses]

		n = math.ceil(ga.cross_prob * len(p))
		if n %2 == 1:
			n -= 1
			ga.population.new_members.append(ga.population.members[random.randint(0,len(p)-1)])

		crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)
		# print("crossover_indices = ",crossover_indexes)

		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]

		for i in range(0,len(crossover_chromosomes)-1,2):
			father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
			crossoverHandler = ga.chooseCrossoverHandler()
			child1, child2 = ga.doCrossover(crossoverHandler,father,mother)
			ga.population.new_members.extend([child1,child2])

		# print("adaptive_mutation value passed = ",ga.adaptive_mutation)

		mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		# print("mutation_indexes = ",mutation_indexes)
		for index in mutation_indexes:
			mutationHandler = ga.chooseMutationHandler()
			ga.population.new_members[index] = ga.doMutation(mutationHandler,ga.population.new_members[index])
		# print("New generation members = ", ga.population.new_members)
		# print("Length of new generation ", len(ga.population.new_members))
		return 0

	def __evolve_pyspark(self,ga):
		"""
		Private method which performs iterations using pyspark

		Parameters :
		-------------
		ga : reference to the GAEngine object

		Outline of Algorithm:
		---------------------
		Selection :
			- Initial population rdd creation
			- Each chromosome is mapped to key-value pair (chromosome , fitness)
			- Depending on type of fitness type fitest chromosomes are selected for crossover
			- The mapped chromosome rdd is transformed to another rdd containing probabilities for crossover 
				which are calculated by normalizing fitness values of each chromosome  

		Crossover :
			- Rdd containing chromosome pairs to be crossed over are created using the probability score calculated
			- New chromosomes are appended to population
		Mutation:
			- Mutation chromosome rdds are created which are transformed to rdd (index, mutated chromosome)
			- Then collect action is applied to get the mutated chromsomes and used  to replace the corresponding members of population

		"""
		from pyspark import SparkContext
		sc = SparkContext.getOrCreate()
		chromosomes_rdd = sc.parallelize(ga.population.members)
		# Fitness Value Mapping and making selection
		mapped_chromosomes_rdd = chromosomes_rdd.map(lambda x: (x,ga.calculateFitness(x)))
		if ga.selection_handler == Utils.SelectionHandlers.best:
			if type(ga.fitness_type) == str:
				if ga.fitness_type == 'max':
					selected_chromosomes = mapped_chromosomes_rdd.top(len(ga.population.members)-math.ceil(ga.cross_prob * len(ga.population.members)),key=lambda x: x[1])
					ga.best_fitness = selected_chromosomes[0]
					selected_chromosomes = [ x[0] for x in selected_chromosomes]
				elif ga.fitness_type == 'min':
					selected_chromosomes = mapped_chromosomes_rdd.takeOrdered(len(ga.population.members)-math.ceil(ga.cross_prob * len(ga.population.members)),key=lambda x: x[1])
					ga.best_fitness = selected_chromosomes[0]
					selected_chromosomes = [ x[0] for x in selected_chromosomes]
			elif type(ga.fitness_type) == tuple or type(ga.fitness_type) == list:
				if ga.fitness_type[0] == 'equal':
					selected_chromosomes = mapped_chromosomes_rdd.takeOrdered(len(ga.population.members)-math.ceil(ga.cross_prob * len(ga.population.members)),key=lambda x: abs(x[1]-ga.fitness_type[1]))
					ga.best_fitness = selected_chromosomes[0]
					selected_chromosomes = [ x[0] for x in selected_chromosomes]
		else:
			selected_chromosomes = ga.handle_selection()
		# print('Members left after selection =  ', selected_chromosomes)
		# print('Best member after selection = ', ga.best_fitness[0])
		# print('Best fitness after selection = ', ga.best_fitness[1])
		ga.population.new_members = selected_chromosomes

		if ga.fitness_type[0] == 'equal':
			if ga.best_fitness[1] == ga.fitness_type[1]:
				return 1

		n = math.ceil(ga.cross_prob * len(ga.population.members))
		if n %2 == 1:
			n -= 1
			ga.population.new_members.append(ga.population.members[random.randint(0,len(ga.population.members)-1)])

		total_fitness = mapped_chromosomes_rdd.map(lambda x: (x[0],x[1]) if x[1] > 0 else (x[0],random.uniform(0.01, 0.02))).values().sum()

		p = mapped_chromosomes_rdd.map(lambda x: (x[0],x[1]/total_fitness)).values().collect()

		p[random.randint(0,len(p)-1)] += (1-sum(p))


		# Crossover Mapping
		crossover_indexes = np.random.choice(len(ga.population.members),n,p=p, replace=False)
		# print("crossover_indices = ",crossover_indexes)
		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]
		crossover_pair_indexes = [(crossover_indexes[i],crossover_indexes[i+1]) for i in range(0,len(crossover_indexes),2)]

		crossover_pair_indexes_rdd = sc.parallelize(crossover_pair_indexes)
		crossover_before = crossover_pair_indexes_rdd.map(lambda x: (ga.population.members[0],ga.population.members[1]))
		crossover_after = crossover_before.map(lambda x:(x,ga.chooseCrossoverHandler()(x[0],x[1])))

		crossover_results = crossover_after.flatMap(lambda x:x[1]).collect()
		ga.population.new_members.extend(crossover_results)

		# Mutation Handling
		# print("adaptive_mutation value passed = ",ga.adaptive_mutation)
		# print("Dynamic Mutation Rate = ", ga.mut_prob)
		
		mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		# print("mutation_indexes = ",mutation_indexes)
		mutation_indexes_rdd = sc.parallelize(mutation_indexes)
		mutation_before = mutation_indexes_rdd.map(lambda x:(x,ga.population.new_members[x]))
		mutation_results = mutation_before.map(lambda x:(x[0],x[1],ga.chooseMutationHandler()(list(x[1])))).collect()

		for entry in mutation_results:
			ga.population.new_members[entry[0]] = entry[2]

		# print("New generation members = ", ga.population.new_members)
		# print("Length of new generation ", len(ga.population.new_members))

	def evolve(self,ga):
		"""
		Invokes the private method __evolve_normal to perform an iteration Genetic Algorithm

		Parameters :
		-------------
		ga : reference to the GAEngine object

		Returns : 1 if optimal solution was found

		"""
		if self.pyspark == False:
			return self.__evolve_normal(ga)
		else:
			return self.__evolve_pyspark(ga)
