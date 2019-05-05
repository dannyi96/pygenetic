import GAEngine,Utils,ChromosomeFactory
factory = ChromosomeFactory.ChromosomeRangeFactory(noOfGenes=8,minValue=0,maxValue=20,duplicates=False)
ga = GAEngine.GAEngine(factory=factory,population_size=20,cross_prob=0.4,mut_prob=0.2,fitness_type=('equal',130),adaptive_mutation=False,use_pyspark=False,efficient_iteration_halt=False)
ga.addCrossoverHandler(Utils.CrossoverHandlers.PMX,1)
ga.addMutationHandler(Utils.MutationHandlers.swap,1)
ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(100)
