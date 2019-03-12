import matplotlib.pyplot as plt

class Statistics:
	"""
	Class to generate Statistics on operation of Genetic Algorithm 
	
	Instance Members:
	-----------------
	max_fitnesses : List containing the maximum fitness scores discovered in each iteration
	iterations : List containing count of each iteration

	"""


	def __init__(self):
		self.max_fitnesses = []
		self.iterations = []
		self.iterationNumber = 1

	def compute(self,max_fitness):
		"""
		Keeps track of max fitness scores of each iteration and iteration number 

		Parameters :
		------------
		max_fitness : float , fitness score after an iteration

		"""

		self.max_fitnesses.append(max_fitness)
		self.iterations.append(self.iterationNumber)
		self.iterationNumber += 1
		print("max fitnesses list = ",self.max_fitnesses)
		print("iteration number   = ",self.iterations)

	def plot(self):
		"""
		Generates a line graph to display change in fitness values over iterations 

		"""
		plt.plot(self.iterations,self.max_fitnesses)
		plt.show()
