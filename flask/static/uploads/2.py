import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=12,minValue=12,maxValue=122,duplicates=True)
ga = GAEngine.GAEngine(factory=factory,population_size=12,cross_prob=0.8,mut_prob=0.8,fitness_type='max',adaptive_mutation=True,use_pyspark=True)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,12)
ga.addMutationHandler(Utils.MutationHandlers.swap,12)
ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(100)
