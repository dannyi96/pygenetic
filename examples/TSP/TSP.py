import sys 
sys.path.append('../../pyGenetic/')

import GAEngine, ChromosomeFactory, Utils
import matplotlib.pyplot as plt
matrix = [[0,172,145,607,329,72,312,120],[172,0,192,494,209,158,216,92],[145,192,0,490,237,75,205,100],[607,494,490,0,286,545,296,489],[329,209,237,286,0,421,49,208],[72,158,75,545,421,0,249,75],[312,216,205,296,49,249,9,194],[120,92,100,489,208,75,194,0]]
	# best sequence i found: 0 5 2 7 1 6 4 3
factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,0,8)
ga = GAEngine.GAEngine(factory,100,fitness_type='min',mut_prob = 0.3)
ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)

	#ga = GAEngine(fitness,8,factory,20)#,fitness_type='equal')
	#ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 9)

ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
ga.addMutationHandler(Utils.MutationHandlers.swap)

ga.setSelectionHandler(Utils.SelectionHandlers.SUS)
ga.setFitnessHandler(Utils.Fitness.TSP, matrix)
	# ga.setSelectionHandler(Utils.SelectionHandlers.basic)
	# Provide max iteration here ???
ga.evolve(100)
fig = ga.statistics.plot_statistics(['best','worst','avg'])
plt.show()
fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
plt.show()