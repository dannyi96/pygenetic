import Population
import ChromosomeFactory
import random

class GAEngine:

	def __init__(self,fitness_func,fitness_type,factory,population_size=100,cross_prob=0.4,mut_prob=0.2,adaptive_mutation=False,smart_fitness=False):
		self.fitness_func = fitness_func
		self.fitness_type = fitness_type
		self.factory = factory
		self.population = Population.Population(factory,population_size)
		self.population_size = population_size
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob
		self.adaptive_mutation = adaptive_mutation
		self.smart_fitness = smart_fitness
		self.crossover_handlers = []
		self.mutation_handlers = []
		self.selection_handler = None

	def addCrossoverHandler(self,crossover_handler):
		self.crossover_handlers.append(crossover_handler)

	def addMutationHandler(self,mutation_handler):
		self.mutation_handlers.append(mutation_handler)

	def setCrossoverProbability(self,cross_prob):
		self.cross_prob = cross_prob

	def setMutationProbability(self,mut_prob):
		self.mut_prob = mut_prob

	def setSelectionHandler(self,selection_handler):
		self.selection_handler = selection_handler

	def calculateAllFitness(self):
		for chromosome in self.population.members:
			print(chromosome)
			print(self.fitness_func(chromosome))

	def execute_mutation(self):
		for chromosome in self.population.members:
			if random.random() <= self.mut_prob:
				new_chromosome = self.mutation_handlers[0](chromosome)
				print(chromosome, " - > ", new_chromosome)
				self.population.new_members.append(new_chromosome)
		print(self.population.new_members)

	def execute_one_evolution(self):
		iteration_size = self.population.population_size
		if iteration_size%2==1:
			iteration_size -= 1
		for i in range(0,iteration_size,2):
			father, mother = self.population.members[i], self.population.members[i+1]
			if random.random() <= self.cross_prob:
				child1, child2 = self.crossover_handlers[0](father,mother)
				self.population.new_members.append(child1)
				self.population.new_members.append(child2)
				print(father, "   ", mother)
				print('becomes')
				print(child1, "   ", child2)
			if random.random() <= self.mut_prob:
				child = self.mutation_handlers[0](father)
				self.population.new_members.append(child)
				print(father , ' - > ', child)
			if random.random() <= self.mut_prob:
				child = self.mutation_handlers[0](mother)
				self.population.new_members.append(child)
				print(mother, ' - > ', child)
		print(self.population.new_members)
		self.calculateAllFitness()

	def select_next_generation(self):
		#self.population.members = self.selection_handler(self.population.members,self.population.new_members)
		self.scores = []
		self.new_scores = []
		for chromosome in self.population.members:
			self.scores.append((self.fitness_func(chromosome),chromosome))
		for chromosome in self.population.new_members:
			self.new_scores.append((self.fitness_func(chromosome),chromosome))
		self.scores.sort(reverse=True)
		self.new_scores.sort(reverse=True)
		self.population.members = [x[1] for x in self.scores[:100]] + [x[1] for x in self.new_scores[:100]]
		self.population.new_members = []
		#print(self.population.members)

	def evolve(self,iterations=20):
		for i in range(iterations):
			self.execute_one_evolution()
			self.select_next_generation()

if __name__ == '__main__':
	#factory = ChromosomeFactory.ChromosomeRegexFactory(int,noOfGenes=4,pattern='0|1')
	#ga = GAEngine(lambda x:sum(x),'MAX',factory,20)
	#print(ga.fitness_func)
	#print(ga.fitness_type)
	#ga.calculateAllFitness()
	import copy
	factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,1,9)
	def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness

	ga = GAEngine(fitness,'MAX',factory,20)
	#print(ga.fitness_func)
	#print(ga.fitness_type)
	#ga.calculateAllFitness()
	def mut(chrom):
		index = random.randint(0,6)
		newchrom = copy.copy(chrom)
		t = newchrom[index]
		newchrom[index] = newchrom[index+1]
		newchrom[index+1] = t
		return newchrom

	def cross(chrom1,chrom2):
		r = random.randint(1,6)
		new_chromosome1 = chrom1[:r]
		for i in chrom2:
			if i not in new_chromosome1:
				new_chromosome1.append(i)
		new_chromosome2 = chrom2[:r]
		for i in chrom1:
			if i not in new_chromosome2:
				new_chromosome2.append(i)
		return new_chromosome1,new_chromosome2

	ga.addCrossoverHandler(cross)
	ga.addMutationHandler(mut)
	ga.evolve(20)
	#ga.execute_one_evolution()
	#ga.calculateAllFitness()
	#ga.select_next_generation()
