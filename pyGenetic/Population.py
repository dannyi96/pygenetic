import ChromosomeFactory

class Population:

	def __init__(self,factory,population_size):
		self.population_size = population_size
		self.members = []
		self.new_members = []
		self.createMembers(factory)

	def createMembers(self,factory):
		for i in range(self.population_size):
			self.members.append(factory.createChromosome())
		print(self.members)









	def fitnessSort(self,fitness_func):
		self.sorted_chromosomes = sorted(self.population.members,key=self.fitness_func,reverse=True)

	def getPercentOfPopulation(self,percent,fitness_func):
		self.sorted_chromosomes = sorted(self.population.members,key=fitness_func,reverse=True)
		return self.sorted_chromosomes[:int(percent*self.population.population_size)]

	def getMaxFitness(self,fitness_func):
		return max([fitness_func(chromosome) for chromosome in self.members])

if __name__ == '__main__':
	factory = ChromosomeFactory.ChromosomeFactory(int,noOfGenes=4,pattern='0|1')
	pop = Population(factory)
	print(pop.members)