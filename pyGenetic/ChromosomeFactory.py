import rstr

class ChromosomeFactory:

	def __init__(self,data_type,noOfGenes,pattern):
		self.data_type = data_type
		self.noOfGenes = noOfGenes
		self.pattern = pattern

	def createChromosome(self):
		l = [rstr.xeger(self.pattern) for i in range(self.noOfGenes)]
		if(self.data_type==int):
			l = [int(x) for x in l]
		return l

if __name__ == '__main__':
	factory = ChromosomeFactory(int,noOfGenes=4,pattern='0|1')
	print(factory.createChromosome())