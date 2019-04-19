class Population:
	"""
	Class contians info on population of candidate solutions

	Instance Members:
	----------------
	population_size : int
	members : List containing the members of population 
	new_members : List containing members of population after each iteration


	"""

	def __init__(self,factory,population_size):
		self.population_size = population_size
		self.members = []
		self.new_members = []
		self.createMembers(factory)

	def createMembers(self,factory):
		"""
		Generates initial meembers of population by invoking one of the methods from
		ChromosomeFactory.py module

		Parameters :
		-------------
		factory : Reference to a method from ChromosomeFactory.py module

		"""

		for i in range(self.population_size):
			self.members.append(factory.createChromosome())

