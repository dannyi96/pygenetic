.. Pygenetic documentation master file, created by
   sphinx-quickstart on Tue Mar 19 23:01:43 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Pygenetic's documentation!
=====================================

Introduction
============

	Efficient Python Genetic Algorithm Framework provides its users a highly efficient and usable way to explore the problem solving ability of Genetic Algorithms. It seeks to reduce the task of solving a problem using genetic algorithms to just choosing the appropriate operators and values which are provided internally. Further, support is also provided for a user to input his own operators for variation or for solving more specific problems.
	Students, teachers, researchers, company employees / entrepreneurs can all use our genetic algorithm framework while experimenting with different Machine Learning Algorithms and observing performance. They can also play around and simulate different Genetic Algorithms online on our website.


Modules
=======

GAEngine Module 
---------------

	"Contains GAEngine Class which is the main driver program which contains and invokes the operators used in Genetic algorithm
	GAEngine keeps track of specific type of operators the user has specified for running the algorithm"

Instance Members
^^^^^^^^^^^^^^^^
	fitness_func : A function argument
				The fitness function to be used, passed as a function argument
	
	fitness_threshold : int
				Threshold at which a candidate solution is considered optimal solution to the problem
	
	factory : Instance of any subclass of ChromosomeFactory class 
				Generates and returns the initial population of candidate solutions
	
	population_size : int
				The number of candidate solutions that can exist after every iteration
	
	cross_prob : float
				The Crossover probability of crossover operation which determines the extent to which crossover between parents
	
	mutation_prob : float
				The mutation probability of mutation operation which determines extent to which candidates should be mutated
	
	fitness_type : string
				Indicates the nature of fitness value (higher/lower/equal) to be considered during selection of candidates
				(default is max)
	
	adaptive_mutation : boolean
				If set rate of mutation of candidates dynamically changes during execution depending on diversity in population
				(default is true)
	
	smart_fitness : boolean
				TO BE DESCRIBED  

Methods
^^^^^^^
	
	addCrossoverHandler(crossover_handler, weight)
		Sets the function to be used for crossover operation

	addMutationHandler(mutation_handler, weight)
		Sets the function to be used for mutation operation

	setCrossoverProbability(cross_prob)
		Sets value for cross_prob instance variable for crossover operation
	
	setMutationProbability(mut_prob)
		Sets value for mut_prob instance variable
	
	setSelectionHandler(selection_handler)
		Sets the function to be used for selection operation
	
	calculateFitness(chromosome)
		Invokes fitness function (fitness_func) to compute the fitness score of a chromosome
	
	generateFitnessDict()
		Generates a  dictionary of (individual, fitness_score) and also stores the dictionary 
		containing fittest chromosome depending on fitness_type(max/min/equal)
	
	handle_selection()
		Invokes generateFitnessDict() and  selection_handler specified 
	
	normalizeWeights()
		Normalizes crossover and mutation handler weights, result is a CDF
	
	chooseCrossoverHandler()
		Selects crossover handler from available handlers based on weightage given to handlers
	
	chooseMutationHandler()
		Selects mutation handler from available handlers based on weightage given to handlers
		
	evolve()
		Invokes evolve method in Evolution module  which Executes the operations of Genetic algorithm till
		a fitness score reaches a threshold or the number of iterations reach max iterations specified by user


ChromosomeFactory Module
------------------------

ChromosomeFactory
^^^^^^^^^^^^^^^^^

	Abstract Class to be inherited for implemention of different 
	ways of generating initial population of chromosomes
	
	* Instance variables :
	
		data_type : type of data of each gene in chromosome

		noOfGenes : number of genes in each chromosome
	
	* Methods :
	
		createChromosome () : Abstract method to be implemented by derived classes



ChromosomeRegexFactory(ChromosomeFactory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
	
	Class derived from ChromosomeFactory, implements the method createChromosome()
	which generates initial population of candidates by using regex module in python
	on genes

	* Instance variables :

		data_type : datatype of each gene
		
		noOfGenes : int ,  number of genes in each chromosome
		
		pattern : string containing individual genes

	* Methods :

		createChromosome() : Generates a chromosome from given genes using python regex module 
							
							Returns : chromosome : List containing individual genes of chromosome 


ChromosomeRangeFactory(ChromosomeFactory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	Class derived from ChromosomeFactory, implements the method createChromosome()
	which generates initial population of candidates by randomly sampling genes from a 
	range of genes


	* Instance variables :

		data_type : datatype of each gene

		noOfGenes : int , number of genes in each chromosome
		
		minValue : int , lower bound of range
		
		maxValue : int , upper bound of range
		
		duplicates : boolean , indicates if gene can be repeated in chromosome

	* Methods :

		createChromosome(self) : Generates a chromosome by randomly sampling genes from a given range
							
								Returns : chromosome : List of genes representing each chromosome 





Contents:

.. toctree::
   :maxdepth: 2

   Introduction




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

