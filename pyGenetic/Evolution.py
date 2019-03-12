from abc import ABC, abstractmethod
import random
import math
import numpy as np
#import pyspark

class BaseEvolution(ABC):
	"""
	Abstract class to be inherited to implement the specific evolution procedure

	Instance Members :
	------------------
	max_iterations ; int

	Methods :
	---------
	evolve() : abstract method to be implemeted by derived classes

	"""

	def __init__(self,max_iterations):
		self.max_iterations = max_iterations

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
	Class inherits from BaseEvolution and contain implementations of abstract 
	evolution method in  BaseEvolution

	Instance Members :
	------------------

	max_iterations : int
	adaptive_mutation : boolean to indicated if rate of mutation should 
						change dynamically during each iteration
	pyspark : boolean to indicated if parallelization should be supported by using pyspark

	"""
	def __init__(self,max_iterations=100,adaptive_mutation=True,pyspark=False):
		BaseEvolution.__init__(self,max_iterations)
		self.adaptive_mutation = adaptive_mutation
		self.pyspark = pyspark

	def __evolve_normal(self,ga):

		"""
		Private method which performs an iteration

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
		print("Best member = ",ga.best_fitness[0])
		print("Best fitness = ",ga.best_fitness[1])
		if ga.best_fitness[1] == ga.fitness_threshold:
			return 1

		fitnesses = []
		total = 0 #This is not being used
		for chromosome in ga.population.members:
			fitness = ga.calculateFitness(chromosome)
			if fitness == 0:
				fitness = random.uniform(0.01, 0.02)
			total += fitness
			fitnesses.append(fitness)

		p = [ elem/sum(fitnesses) for elem in fitnesses]
		#print("p = ",p)
		n = math.ceil(ga.cross_prob * len(p))
		if n %2 == 1:
			n -= 1
			ga.population.members.append(ga.population.members[0])

		crossover_indexes = np.random.choice(len(p),n,p=p, replace=False)
		#print("crossover_indices = ",crossover_indexes)

		crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]

		for i in range(0,len(crossover_chromosomes)-1,2):
			father,mother = crossover_chromosomes[i], crossover_chromosomes[i+1]
			crossoverHandler = ga.chooseCrossoverHandler()
			child1, child2 = crossoverHandler(father,mother)
			ga.population.new_members.extend([child1,child2])
		print("adaptive_mutation value passed = ",self.adaptive_mutation)

		if self.adaptive_mutation == True:
			mean_fitness = sum(fitnesses)/len(fitnesses)
			average_square_deviation = math.sqrt(sum((fitness - mean_fitness)**2 for fitness in fitnesses)) / len(fitnesses)
			ga.dynamic_mutation = ga.mut_prob * ( 1 + ( (ga.best_fitness[1]-average_square_deviation) / (ga.best_fitness[1]+average_square_deviation) ) )
			print('Adaptive mutation value = ',ga.dynamic_mutation)
			mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.dynamic_mutation*len(p)), replace=False)
		else:
			mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		for index in mutation_indexes:
			mutationHandler = ga.chooseMutationHandler()
			ga.population.new_members[index] = mutationHandler(ga.population.new_members[index])
		ga.population.members = ga.population.new_members
		#print("New members = ",ga.population.members)
		ga.population.new_members = []

	def __evolve_pyspark(self,ga):
		from pyspark import SparkContext
		sc = SparkContext.getOrCreate()
		#print(ga.population.members)
		chromosomes_rdd = sc.parallelize(ga.population.members)
		# Fitness Value Mapping and making selection
		mapped_chromosomes_rdd = chromosomes_rdd.map(lambda x: (x,ga.calculateFitness(x)))
		#print(mapped_chromosomes_rdd.collect())
		selected_chromosomes = mapped_chromosomes_rdd.takeOrdered(len(ga.population.members)-math.ceil(ga.cross_prob * len(ga.population.members)),key=lambda x: x[1])
		#selected_chromosomes = mapped_chromosomes_rdd.top(len(ga.population.members)-math.ceil(ga.cross_prob * len(ga.population.members)),key=lambda x: x[1])
		#print(selected_chromosomes)
		ga.best_fitness = selected_chromosomes[0]
		print('BEST', ga.best_fitness[1])
		ga.population.new_members = [x[0] for x in selected_chromosomes]
		#print(ga.population.new_members)
		#exit()
		n = math.ceil(ga.cross_prob * len(ga.population.members))
		if n %2 == 1:
			n -= 1
			ga.population.members.append(ga.population.members[0])

		total_fitness = mapped_chromosomes_rdd.values().sum()
		#print(total_fitness)
		#print(type(total_fitness))
		p = mapped_chromosomes_rdd.map(lambda x: (x[0],x[1]/total_fitness)).values().collect()
		#print(p)
		#print(type(p))
		#print(sum(p))

		# Crossover Mapping
		crossover_indexes = np.random.choice(len(ga.population.members),n,p=p, replace=False)
		#print("crossover_indices = ",crossover_indexes)
		#crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]

		crossover_pair_indexes = [(crossover_indexes[i],crossover_indexes[i+1]) for i in range(0,len(crossover_indexes),2)]
		#print(crossover_indexes)
		#print(crossover_pair_indexes)
		
		crossover_pair_indexes_rdd = sc.parallelize(crossover_pair_indexes)
		crossover_before = crossover_pair_indexes_rdd.map(lambda x: (ga.population.members[0],ga.population.members[1]))
		#print(crossover_before.collect())
		crossover_results = crossover_before.map(lambda x:(x,ga.chooseCrossoverHandler()(x[0],x[1])))#.flatmap
		#print(crossover_results.collect())
		result_test = crossover_results.flatMap(lambda x:x[1]).collect()
		#print(result_test)
		#print(type(result_test))

		ga.population.new_members.extend(result_test)

		#print(len(ga.population.members))
		#print(len(ga.population.new_members))
		#print(ga.population.new_members)

		# Mutation Handling
		mutation_indexes = np.random.choice(len(ga.population.new_members),int(ga.mut_prob*len(p)), replace=False)
		#print(mutation_indexes)
		mutation_indexes_rdd = sc.parallelize(mutation_indexes)
		mutation_results = mutation_indexes_rdd.map(lambda x:(x,ga.population.new_members[x]))
		#print(mutation_results.collect())
		mutation_results = mutation_results.map(lambda x:(x[0],x[1],ga.chooseMutationHandler()(list(x[1])))).collect()
		#print(mutation_results)
		#print('BEFORE')
		#print(ga.population.new_members)
		for entry in mutation_results:
			ga.population.new_members[entry[0]] = entry[2]

		#print('AFTER')
		#print(ga.population.new_members)

		ga.population.members = ga.population.new_members 
		ga.population.new_members = []


		# Crossover Mapping
		#crossover_indexes = np.random.choice(len(ga.population.members),n,p=p, replace=False)
		#print("crossover_indices = ",crossover_indexes)
		#crossover_chromosomes = [ ga.population.members[index] for index in crossover_indexes]








	def evolve(self,ga):
		"""
		Invokes the private method __evolve_normal to perform an iteration Genetic Algorithm

		Returns : 1 if optimal solution was found

		"""
		#print(self.max_iterations)
		if self.pyspark == False:
			if self.__evolve_normal(ga):
				return 1
		else:
			if self.__evolve_pyspark(ga):
				return 1
