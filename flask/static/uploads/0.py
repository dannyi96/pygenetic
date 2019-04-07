import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=7,minValue=10,maxValue=30,duplicates=False)
ga = GAEngine.GAEngine(factory=factory,population_size=100,cross_prob=0.3,mut_prob=0.5,fitness_type='max',adaptive_mutation=True,use_pyspark=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct,3)
ga.addMutationHandler(Utils.MutationHandlers.swap,4)
ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(10)
