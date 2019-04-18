import sys 
sys.path.append('../../pyGenetic/')

import GAEngine, ChromosomeFactory, Utils
import matplotlib.pyplot as plt
import time

# Normal execution
matrix = [[0,172,145,607,329,72,312,120],[172,0,192,494,209,158,216,92],[145,192,0,490,237,75,205,100],[607,494,490,0,286,545,296,489],[329,209,237,286,0,421,49,208],[72,158,75,545,421,0,249,75],[312,216,205,296,49,249,9,194],[120,92,100,489,208,75,194,0]]
	# best sequence i found: 0 5 2 7 1 6 4 3


times = []
#a = time.time()
#ga.evolve(100)
#b = time.time()
#print(b-a)


for i in range(1,11):
	factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=0,maxValue=7,data_type=int)
	ga = GAEngine.GAEngine(factory,population_size=10000,fitness_type='min',mut_prob = 0.02)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
	ga.addMutationHandler(Utils.MutationHandlers.swap)
	ga.setSelectionHandler(Utils.SelectionHandlers.SUS)
	ga.setFitnessHandler(Utils.Fitness.TSP, matrix)
	start_time = time.time()
	ga.evolve(i)
	end_time = time.time()
	time_taken = end_time - start_time
	times.append(time_taken)
	print(time_taken)
	print(times)
	time.sleep(2)


fig,ax = plt.subplots()
print(times)
ax.plot(range(len(times)),times,label='without pyspark')
fig.legend(loc='upper left')
plt.show()

for i in range(1,11):
	factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=0,maxValue=7,data_type=int)
	ga = GAEngine.GAEngine(factory,population_size=10000,fitness_type='min',mut_prob = 0.02,use_pyspark=True)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
	ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
	ga.addMutationHandler(Utils.MutationHandlers.swap)
	ga.setSelectionHandler(Utils.SelectionHandlers.SUS)
	ga.setFitnessHandler(Utils.Fitness.TSP, matrix)
	start_time = time.time()
	ga.evolve(i)
	end_time = time.time()
	time_taken = end_time - start_time
	times.append(time_taken)
	print(time_taken)
	print(times)
	time.sleep(2)

ax.plot(range(len(times)),times,label='with pyspark')
fig.legend(loc='upper left')
plt.show()
