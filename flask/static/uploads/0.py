import GAEngine
import Utils
import ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(data_type=int,noOfGenes=8,minValue=0,maxValue=20,duplicates=False)
ga = GAEngine.GAEngine(factory=factory,population_size=20,cross_prob=0.4,mut_prob=0.2,fitness_type='max',adaptive_mutation=True,use_pyspark=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.onePoint,1)
ga.addMutationHandler(Utils.MutationHandlers.swap,4)
ga.setSelectionHandler(Utils.SelectionHandlers.basic)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(10)
