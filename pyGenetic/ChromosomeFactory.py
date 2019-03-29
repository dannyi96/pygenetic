from abc import ABC, abstractmethod
import rstr
import random
import re

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

	def __init__(self,noOfGenes,data_type):
		self.noOfGenes = noOfGenes
		self.data_type = data_type

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

	def __init__(self,noOfGenes,pattern,data_type=str):
		"""
		Parameters :
		------------

		data_type : datatype of each gene
		noOfGenes : int ,  number of genes in each chromosome
		pattern : string containing individual genes

		"""

		if noOfGenes <= 0:
			raise ValueError('No of genes cannot be negative or zero')
		if data_type not in [str,int,float]:
			raise ValueError('Invalid datatype given to Chromosome Regex Factory')
		try:
			re.compile(pattern)
		except re.error:
			raise ValueError('Invalid regex given to Chromosome Regex Factory')

		ChromosomeFactory.__init__(self,noOfGenes,data_type)
		self.pattern = pattern
		

	def createChromosome(self):
		"""
		Generates a chromosome from given genes using python regex module

		Returns :
		---------
		chromosome : List containing individual genes of chromosome

		"""
		try:
			if self.data_type == int:
				chromosome = [int(rstr.xeger(self.pattern)) for i in range(self.noOfGenes)]
			elif self.data_type == float:
				chromosome = [float(rstr.xeger(self.pattern)) for i in range(self.noOfGenes)]
			else:
				chromosome = [rstr.xeger(self.pattern) for i in range(self.noOfGenes)]
			return chromosome
		except:
			raise Exception('Unable to convert all/some strings of given regex to type %s'%(type(self.data_type).__name__))
		

class ChromosomeRangeFactory(ChromosomeFactory):
	"""
	Class derived from ChromosomeFactory, implements the method createChromosome()
	which generates initial population of candidates by randomly sampling genes from a
	range of genes

	"""

	def __init__(self,noOfGenes,minValue,maxValue,duplicates=False,data_type=int):
		"""
		Parameters :
		-----------

		data_type : datatype of each gene
		noOfGenes : int , number of genes in each chromosome
		minValue : int , lower bound of range
		maxValue : int , upper bound of range
		duplicates : boolean , indicates if gene can be repeated in chromosome

		"""

		if noOfGenes <= 0 :
			raise ValueError('No of genes cannot be negative')

		if minValue > maxValue:
			raise ValueError('minValue cannot be greater than maxValue')

		if type(duplicates) != bool:
			raise ValueError('Invalid duplicated value given')


		ChromosomeFactory.__init__(self,noOfGenes,data_type)
		self.minValue = minValue
		self.maxValue = maxValue
	
	def createChromosome(self):
		"""
		Generates a chromosome by randomly sampling genes from a given range

		Returns :
		---------
		chromosome : List of genes representing each chromosome

		"""
		print(self.minValue,"++++",self.maxValue)
		try:
			chromosome = random.sample(range(self.minValue,self.maxValue), self.noOfGenes)
			return chromosome
		except:
			raise Exception('Unable to generated sample from given max %s min %s noOfGenes %s'%(self.minValue,self.maxValue,self.noOfGenes))


if __name__ == '__main__':
	print("Entered main in chromosome factory")
	#factory1 = ChromosomeRegexFactory(int,noOfGenes=4,pattern='0|1|7')
	#print(factory1.createChromosome())
	#factory2 = ChromosomeRangeFactory(int,8,3,11)
	#print(factory2.createChromosome())
	factory = ChromosomeRegexFactory(noOfGenes=3,pattern='a|B|c',data_type=str)
	print(factory.createChromosome())
