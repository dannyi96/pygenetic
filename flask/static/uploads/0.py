import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=,pattern='')
ga = GAEngine.GAEngine(factory=factory,population_size=,cross_prob=,mut_prob=,fitness_type='max',adaptive_mutation=True,use_pyspark=True)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,)
ga.addMutationHandler(Utils.MutationHandlers.swap,)
ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve()
