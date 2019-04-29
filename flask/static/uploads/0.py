import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=10,minValue=100,maxValue=200,duplicates=True)
ga = GAEngine.GAEngine(factory=factory,population_size=100,cross_prob=0.3,mut_prob=0.3,fitness_type='max',adaptive_mutation=True,use_pyspark=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,3)
ga.addMutationHandler(Utils.MutationHandlers.swap,3)
ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(20)
