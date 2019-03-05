import matplotlib.pyplot as plt

class Statistics:
	def __init__(self):
		self.max_fitnesses = []
		self.iterations = []
		self.iterationNumber = 1

	def compute(self,max_fitness):
		self.max_fitnesses.append(max_fitness)
		self.iterations.append(self.iterationNumber)
		self.iterationNumber += 1
		print(self.max_fitnesses)
		print(self.iterations)

	def plot(self):
		plt.plot(self.iterations,self.max_fitnesses)
		plt.show()