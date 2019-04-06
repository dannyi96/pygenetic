import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=10,minValue=1,maxValue=20,duplicates=True)
ga = GAEngine.GAEngine(factory=factory,population_size=100,cross_prob=0.3,mut_prob=0.4,fitness_type='max',adaptive_mutation=True,use_pyspark=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,2)
ga.addMutationHandler(Utils.MutationHandlers.swap,4)
ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(100)
