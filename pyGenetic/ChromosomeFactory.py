from abc import ABC, abstractmethod
import rstr
import random

class ChromosomeFactory(ABC):

	def __init__(self,data_type,noOfGenes):
		self.data_type = data_type
		self.noOfGenes = noOfGenes

	@abstractmethod
	def createChromosome(self):
		pass

class ChromosomeRegexFactory(ChromosomeFactory):

	def __init__(self,data_type,noOfGenes,pattern):
		ChromosomeFactory.__init__(self,data_type,noOfGenes)
		self.pattern = pattern

	def createChromosome(self):
		if self.data_type==int:
			chromosome = [int(rstr.xeger(self.pattern)) for i in range(self.noOfGenes)]
		else:
			chromosome = [rstr.xeger(self.pattern) for i in range(self.noOfGenes)]
		return chromosome

class ChromosomeRangeFactory(ChromosomeFactory):

	def __init__(self,data_type,noOfGenes,minValue,maxValue,duplicates=False):
		ChromosomeFactory.__init__(self,data_type,noOfGenes)
		self.minValue = minValue
		self.maxValue = maxValue

	def createChromosome(self):
		chromosome = random.sample(range(self.minValue,self.maxValue), self.noOfGenes)
		return chromosome

if __name__ == '__main__':
	factory1 = ChromosomeRegexFactory(int,noOfGenes=4,pattern='0|1|7')
	print(factory1.createChromosome())
	factory2 = ChromosomeRangeFactory(int,8,3,11)
	print(factory2.createChromosome())