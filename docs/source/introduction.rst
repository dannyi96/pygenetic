Introduction
============

	Pygenetic provides users a highly efficient and usable way to explore the problem solving ability of Genetic Algorithms. It seeks to reduce the task of solving a problem using genetic algorithms to just choosing the appropriate operators and values which are provided internally. Further, support is also provided for a user to input his own operators for variation or for solving more specific problems.
	Students, teachers, researchers, company employees / entrepreneurs can all use our genetic algorithm framework while experimenting with different Machine Learning Algorithms and observing performance.



Features
********

   - Presence of both High-Level(SimpleGA) and Low-Level API(GAEngine) which users can use as per need.
   - Very generic API - Users can customize different part of the GA be it Evolution, Statistics, Different handlers, Chromosome Representations.
   - Supports efficient evolution execution using Apache Spark. This is highly scalable as more workers can be deployed. Parallelization of fitness evaluation, 	selection, crossovers and mutations are taken care of.
   - Supports Adaptive Mutation Rates based on how diverse the population is.
   - Supports Hall of Fame(best ever chromosome) Injection so that the best chromosome isn't lost in later generations due to the selection method used.
   - Supports Efficient Iteration Halt
   - Supports Visualization of Statistics like max, min, avg, diversity of fitnesses, mutation rates. Users can also define custom statistics
   - Supports usage of multiple crossovers and mutations in one GA execution to enhance diversity
   - Supports Population Control which users can make use of in various research purposes
   - Provides a bunch of Standard Selection, Crossovers, Mutations and Fitness Functions
   - Provides continue evolve feature so users can continue from previous evolutions instead of starting all over again.
   - Provides ANN Best Topology finder using GA functionality



