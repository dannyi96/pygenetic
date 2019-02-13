import random
import copy
#class SelectionHandlers:



class MutationHandlers:
	@staticmethod
	def swap(chromosome):
		index = random.randint(0,len(chromosome)-2)
		newchrom = copy.copy(chromosome)
		newchrom[index], newchrom[index+1] = newchrom[index+1], newchrom[index]
		return newchrom

#class CrossoverHandlers: