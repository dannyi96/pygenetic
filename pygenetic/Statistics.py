import matplotlib
import os
if 'TRAVIS' in os.environ:
    print('Warning: no DISPLAY environment variable found. Using matplotlib non-interactive Agg backend')
    matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Statistics:
	"""
	Class to generate Statistics on operation of Genetic Algorithm

	Instance Members:
	-----------------
	statistic_dict : A dictionary storing different statistics mapped to list storing each generation data
				Stats stored are best-fitness, worst-fitness, avg-fitness, diversity and mutation-rate

	"""


	def __init__(self):
		self.statistic_dict = {'best-fitness':[],'worst-fitness':[],'avg-fitness':[],'diversity':[],'mutation_rate':[]}

	def add_statistic(self,statistic,value):
		"""
		Appends a value to specified statistic, usually called after each iteration

		Parameters :
		------------
		statistic : The statistic for which the value is relevant and is to be appended
		value : Th evalue to be appended

		"""
		if statistic in self.statistic_dict:
			self.statistic_dict[statistic].append(value)
		else:
			self.statistic_dict[statistic] = [value]


	def plot(self):
		"""
		Generates a line graph for each statistic to display change over iterations

		"""
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		for statistic in self.statistic_dict:
			ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig

	def plot_statistics(self,statistics):
		"""
		Generates a line graph for list of specified statistics to display change over iterations

		Parameters :
		----------
		statistics : A list of statistic names whose variation is to be shown

		"""
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		for statistic in statistics:
			ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig

	def plot_statistic(self,statistic):
		"""
		Generates a line graph for specified statistic to display change over iterations

		Parameters :
		----------
		statistic : The statistic name whose variation is to be shown

		"""
		fig,ax = plt.subplots()
		ax.set_xlabel('Generation')
		ax.set_ylabel('Statistic')
		ax.plot(range(1,len(self.statistic_dict[statistic])+1),self.statistic_dict[statistic],label=statistic)
		fig.legend(loc='upper left')
		return fig
