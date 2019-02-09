import Population
import ChromosomeFactory

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

	def addCrossoverHandler(self,crossover_handler):
		self.crossover_handlers.append(crossover_handler)

	def addMutationHandler(self,mutation_handler):
		self.mutation_handlers.append(mutation_func)

	def setCrossoverProbability(self,cross_prob):
		self.cross_prob = cross_prob

	def setMutationProbability(self,mut_prob):
		self.mut_prob = mut_prob

	def calculateAllFitness(self):
		for chromosome in self.population.members:
			print(chromosome)
			print(self.fitness_func(chromosome))


if __name__ == '__main__':
	factory = ChromosomeFactory.ChromosomeFactory(int,noOfGenes=4,pattern='0|1')
	ga = GAEngine(lambda x:sum(x),'MAX',factory,20)
	print(ga.fitness_func)
	print(ga.fitness_type)
	ga.calculateAllFitness()