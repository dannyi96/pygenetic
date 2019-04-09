import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=14,minValue=1,maxValue=15,duplicates=True)
ga = GAEngine.GAEngine(factory=factory,population_size=100,cross_prob=,mut_prob=0.3,fitness_type=('equal', 14.0),adaptive_mutation=True,use_pyspark=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,0.3)
ga.addMutationHandler(Utils.MutationHandlers.swap,0.3)
ga.setSelectionHandler(Utils.SelectionHandlers.largest)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(100)
