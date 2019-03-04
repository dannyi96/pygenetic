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
		#print(self.members)

if __name__ == '__main__':
	factory = ChromosomeFactory.ChromosomeFactory(int,noOfGenes=4,pattern='0|1')
	pop = Population(factory)
	print(pop.members)