from pygenetic import GAEngine, ChromosomeFactory, Utils
import matplotlib.pyplot as plt
matrix = [[0,172,145,607,329,72,312,120],[172,0,192,494,209,158,216,92],[145,192,0,490,237,75,205,100],[607,494,490,0,286,545,296,489],[329,209,237,286,0,421,49,208],[72,158,75,545,421,0,249,75],[312,216,205,296,49,249,9,194],[120,92,100,489,208,75,194,0]]
	# best sequence i found: 0 5 2 7 1 6 4 3
factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=0,maxValue=7)
ga = GAEngine.GAEngine(factory,10,fitness_type='min',mut_prob = 0.02)
ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
ga.addMutationHandler(Utils.MutationHandlers.swap)
ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(Utils.Fitness.TSP, matrix)

ga.evolve(100)
fig = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
plt.show()
fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
plt.show()
fig = ga.statistics.plot_statistics(['mutation_rate'])
plt.show()

ga.continue_evolve(20)

fig = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
plt.show()
fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
plt.show()
fig = ga.statistics.plot_statistics(['mutation_rate'])
plt.show()

ga.evolve(30)
fig = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
plt.show()
fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
plt.show()
fig = ga.statistics.plot_statistics(['mutation_rate'])
plt.show()
