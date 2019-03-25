from abc import ABC, abstractmethod
import rstr
import random

class ChromosomeFactory(ABC):
	"""
	Abstract Class to be inherited for implemention of different
	ways of generating initial population of chromosomes

	Instance variables :
	------------------
	data_type : type of data of each gene in chromosome
	noOfGenes : number of genes in each chromosome

	Methods :
	---------
	createChromosome () : Abstract method to be implemented by derived classes

	"""

	def __init__(self,data_type,noOfGenes):
		self.data_type = data_type
		self.noOfGenes = noOfGenes

	@abstractmethod
	def createChromosome(self):
		"""
		Abstract method to be implemented by derived classes

		"""
		pass

class ChromosomeRegexFactory(ChromosomeFactory):
	"""
	Class derived from ChromosomeFactory, implements the method createChromosome()
	which generates initial population of candidates by using regex module in python
	on genes

	"""

	def __init__(self,data_type,noOfGenes,pattern):
		"""
		Parameters :
		------------

		data_type : datatype of each gene
		noOfGenes : int ,  number of genes in each chromosome
		pattern : string containing individual genes

		"""

		try : 

			if noOfGenes < 0:
				raise ValueError('No of genes cannot be negative')

			ChromosomeFactory.__init__(self,data_type,noOfGenes)
			self.pattern = pattern
		
		except ValueError as ve :
			print(ve)

	def createChromosome(self):
		"""
		Generates a chromosome from given genes using python regex module

		Returns :
		---------
		chromosome : List containing individual genes of chromosome

		"""

		if self.data_type==int:
			chromosome = [int(rstr.xeger(self.pattern)) for i in range(self.noOfGenes)]
		else:
			chromosome = [rstr.xeger(self.pattern) for i in range(self.noOfGenes)]
		return chromosome

class ChromosomeRangeFactory(ChromosomeFactory):
	"""
	Class derived from ChromosomeFactory, implements the method createChromosome()
	which generates initial population of candidates by randomly sampling genes from a
	range of genes

	"""

	def __init__(self,data_type,noOfGenes,minValue,maxValue,duplicates=False):
		"""
		Parameters :
		-----------

		data_type : datatype of each gene
		noOfGenes : int , number of genes in each chromosome
		minValue : int , lower bound of range
		maxValue : int , upper bound of range
		duplicates : boolean , indicates if gene can be repeated in chromosome

		"""

		try:
			if noOfGenes < 0 :
				raise ValueError('No of genes cannot be negative')

			if minValue > maxValue:
				raise ValueError('minValue cannot be greater than maxValue')


			ChromosomeFactory.__init__(self,data_type,noOfGenes)
			self.minValue = minValue
			self.maxValue = maxValue

		except ValueError as ve:
			print(ve)
	
	def createChromosome(self):
		"""
		Generates a chromosome by randomly sampling genes from a given range

		Returns :
		---------
		chromosome : List of genes representing each chromosome

		"""

		chromosome = random.sample(range(self.minValue,self.maxValue), self.noOfGenes)
		return chromosome


if __name__ == '__main__':
	print("Entered main in chromosome factory")
	factory1 = ChromosomeRegexFactory(int,noOfGenes=4,pattern='0|1|7')
	print(factory1.createChromosome())
	factory2 = ChromosomeRangeFactory(int,8,3,11)
	print(factory2.createChromosome())
