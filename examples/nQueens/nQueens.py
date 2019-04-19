import sys 
sys.path.append('../../pyGenetic/')

import GAEngine, ChromosomeFactory, Utils
import matplotlib.pyplot as plt

def fitness(board):
		fitness = 0
		for i in range(len(board)):
			isSafe = True
			for j in range(len(board)):
				if i!=j:
					if (board[i] == board[j]) or (abs(board[i] - board[j]) == abs(i-j)):
						isSafe = False
						break
			if(isSafe==True):
				fitness += 1
		return fitness


factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=14,minValue=1,maxValue=14)
ga = GAEngine.GAEngine(factory,100,fitness_type=('equal',14),mut_prob = 0.3)

#ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)

ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
#ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
ga.addMutationHandler(Utils.MutationHandlers.swap)
# SOme issue with roullete
ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(fitness)

ga.evolve(10)

fig = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
plt.show()
fig = ga.statistics.plot_statistics(['diversity','mutation_rate'])
plt.show()