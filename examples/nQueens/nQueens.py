import sys 
sys.path.append('../../pyGenetic/')

import GAEngine, ChromosomeFactory, Utils

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

factory = ChromosomeFactory.ChromosomeRangeFactory(int,8,1,9)
ga = GAEngine.GAEngine(8,factory,100,fitness_type='equal',mut_prob = 0.001)
#ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX, 9)

ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
#ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
ga.addMutationHandler(Utils.MutationHandlers.swap)

ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(fitness)

ga.evolve(100)