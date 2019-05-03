import matplotlib
import os
if os.environ.get('DISPLAY','') == '':
    print('Warning: no DISPLAY environment variable found. Using matplotlib non-interactive Agg backend')
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
		self.statistic_dict = {'best-fitness':[],'worst-fitness':[],'avg-fitness':[],'diversity':[],'mutation_rate':[]}

	def add_statistic(self,statistic,value):
		"""
		Keeps track of max fitness scores of each iteration and iteration number

		Parameters :
		------------
		max_fitness : float , fitness score after an iteration

		"""
		if statistic in self.statistic_dict:
			self.statistic_dict[statistic].append(value)
		else:
			self.statistic_dict[statistic] = [value]


	def plot(self):
		"""
		Generates a line graph to display change in fitness values over iterations

		"""
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		for statistic in self.statistic_dict:
			print(statistic,self.statistic_dict[statistic])
			ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig

	def plot_statistics(self,statistics):
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		for statistic in statistics:
			print(statistic,self.statistic_dict[statistic])
			ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig

	def plot_statistic(self,statistic):
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig
