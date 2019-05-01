# Usage of pygenetic: An overview
## 1. Usage of `GAEngine`: the Low Level pygenetic GA API 
### 1.1 Creating a Chromosome Factory
Chromosome Factories specify how the chromosome for the GA is to be created.

pygenetic supports two types of `ChromosomeFactories`
* `ChromosomeRegexFactory`: for creating chromosomes whose genes follow a particular regex
* `ChromosomeRangeFactory`: for creating chromosomes whose genes are between some numeric interval

#### 1.1.1 Usage of ChromosomeRangeFactory
```
>>> from pygenetic import ChromosomeFactory
>>> factory = ChromosomeFactory.ChromosomeRangeFactory(minValue=1,
                        maxValue=100,noOfGenes=8,duplicates=False)
```
This creates a factory to create chromosomes with 8 genes and those genes can take values between 1 and 100 with no duplicates

We can test if it creates chromosomes as expected by calling the `createChromosome` method of the factory
```
>>> factory.createChromosome()
[62, 24, 10, 84, 93, 40, 86, 87]
```

#### 1.1.2 Usage of ChromosomeRegexFactory
```
>>> factory = ChromosomeFactory.ChromosomeRegexFactory(pattern='0|1|7',noOfGenes=10,data_type=int)
>>> factory.createChromosome()
[7, 7, 7, 0, 0, 0, 7, 1, 1, 7]
```
This creates a factory to create chromosomes with 10 genes and those genes can take values from the regex `0|1|7` with the genes converted to an integer data type.

#### 1.1.3 Custom Chromosome Factories

Users can easily define custom factories by subclassing `ChromosomeFactory`

```
>>> class CustomFactory(ChromosomeFactory.ChromosomeFactory):
...     def __init__(self,noOfGenes,input_list):
...             self.noOfGenes = noOfGenes
...             self.input_list = input_list
...     def createChromosome(self):
...             return random.sample(self.input_list,self.noOfGenes)
... 
>>> factory = CustomFactory(noOfGenes=5,input_list=['duck','cow',
                              'monkey','giraffe','dog','cat','peacock','mice','sun'])
>>> factory.createChromosome()
['mice', 'giraffe', 'cow', 'dog', 'cat']
```

This factory creates a chromosomes whose values are taken from values given in an input list.

### 1.2 Defining the GA using `GAEngine`

We can now create the `GAEngine` which is responsible for running the GA.

It can easily created using the factory created earlier

```
>>> from pygenetic import GAEngine
>>> ga = GAEngine.GAEngine(factory=factory,population_size=100,fitness_type=('equal',8),
				cross_prob=0.7,mut_prob = 0.1)
```
where `factory` is the ChromosomeFactory to be used in the GA
      `population_size` is the size of population to be used in the GA
      `fitness_type` is the fitness type which can be either `max`, `min` or `(equal,<value-to-acheive>)`
      `cross_prob` is the crossover probability
      `mut_prob` is the mutation probability
      
Other parameters of `GAEngine` include
* `adaptive_mutation`: which is a Boolean which decides if adaptive mutation is to be used(default: True) 
* `population_control`: which is a Boolean which decides whether or not the GAEngine should ensure that the population size remains the same in every evolution iteration. This ensures that any error/issue in user's custom selection or evolution code doesn't cause population size to change. (default: False)
* `hall_of_fame_injection`: which is a boolean used to carry out the injection of the best chromosome encountered so far in every 20 generations. (default: True)
* `efficient_iteration_halt`: which is a boolean used to carry out efficient_iteration_halt optimization. It stops evolving if same best fitness value is encountered for 20 consecutive generations (default: True)
* `use_pyspark`: which is a boolean used to decide if sequential execution is to be carried out or parallel execution on Apache Spark is to be carried out (default: False)

### 1.3 Crossovers, Mutations and Selection Functions

#### 1.3.1 Basics

We should then add appropriate Crossovers, Mutations and Selection Functions for our GA execution

Many standard Crossovers, Mutations and Selection Functions are already available in `Utils` of `pygenetic` module. 
Utils contains the following
1. Selection - `random`, `best`, `tournament`, `roulette`, `rank` and `SUS`
2. Crossover - `distinct`, `onePoint`, `twoPoint`, `PMX` and `OX`
3. Mutation - `swap` and `bitFlip`

`pygenetic` supports more than one crossovers and mutations in one GA execution.
```
from pygenetic import Utils
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct, 4)
ga.addCrossoverHandler(Utils.CrossoverHandlers.OX, 3)
ga.addMutationHandler(Utils.MutationHandlers.swap,2)
```
where the first parameter is the handler and the second parameter is the weightage to be given to that handler.

Note: for handlers which require parameters (eg: `tournament`), the parameters are passed after the weight parameter when added to the `GAEngine` object
```
from pygenetic import Utils
# 4 is the weightage while 2 is the parameter of the handler(tournament size)
ga.addCrossoverHandler(Utils.CrossoverHandlers.tournament, 4, 2)
```

We can also add selection handler in the same fashion
```
ga.setSelectionHandler(Utils.SelectionHandlers.best)
```

#### 1.3.2 Custom Handlers

Users can also define custom Crossovers, Mutations and Selection handlers where the function follows the prototype
```def custom_function(fitness_mappings, ga)```
where `fitness_mappings` is a list of tuples where each tuple is of the form `(chromosome,fitness_score)`
      `ga` is the entire `GAEngine` object which user would created. A user can access any detail regarding the GA over here.
      (Note: use `ga.population.members` to access current population members)

Note: Crossover and Mutation handlers should return a tuple of the two new children while Selection handlers should return a list of selected chromosomes.

It can be added as always
```
ga.addCrossoverHandler(custom_function, 4)
ga.addMutationHandler(custom_function2,2)
ga.setSelectionHandler(custom_function3)
```

Users can also define parameterized custom Crossovers, Mutations and Selection handlers where the function follows the prototype
```def custom_function (fitness_mappings, ga, ...)```
where `fitness_mappings` is a list of tuples where each tuple is of the form `(chromosome,fitness_score)`
      `ga` is the entire `GAEngine` object which user would created. A user can access any detail regarding the GA over here.
      `...` are any other arguments needed
It can be added as always
```
# where 4 is the weightage
ga.addCrossoverHandler(custom_function, 4, ...)
ga.addMutationHandler(custom_function2, 2, ...)
ga.setSelectionHandler(custom_function3)
```

### 1.4 Adding fitness function of the GA

Users can define their custom fitness function and add it to the GA.

A typical fitness signature would be `def fitness(chromosome)`

```
def fitness(chromosome):
  return sum(chromosome)
```

It can be added like
`ga.setFitnessHandler(fitness)`

For fitness functions which depend on more than just the chromosome(eg: in TSP), we can add more parameters like `def fitness(chromosome,...)`

Eg: In TSP
```
def TSP(chromosome, matrix):
		total = 0
		for i in range(len(chromosome)-1):
			total += matrix[chromosome[i]][chromosome[i+1]]
		return total  
ga.setFitnessHandler(fitness,TSP_matrix)
```

### 1.5 Running the GA

The GA can now be executed
`ga.evolve(20)`
where the parameter to be given is the number of GA iterations to be executed

In case, you feel you want to continue from a previous execution, you can
`ga.continue_evolve(20)`

We can obtain the best member after the evolution by
```
print(ga.best_fitness)
```
This returns a tuple where the first element is the best chromosome and the second element is the corresponding best fitness value

### 1.6 Statistics

By default, we can view the following GA statistics after Evolution - `'best-fitness','worst-fitness','avg-fitness','diversity', 'mutation_rate'`

We can plot graphs for this 
```
import matplotlib.pyplot as plt
fig = ga.statistics.plot_statistics(['best-fitness','worst-fitness','avg-fitness'])
plt.show()
```

We can also define custom Statistics and add it to the GA
```
def range_of_generation(fitness_mappings,ga):
	return abs(fitness_mappings[0][1] - fitness_mappings[-1][1])

ga.addStatistic('range',range_of_generation)
# After evolutions
fig = ga.statistics.plot_statistics(['range'])
plt.show()
```

### 1.7 Custom Evolutions

Users can define some custom evolution by subclassing `BaseEvolution` and filling `ga.population.new_members` with the new members from the evolution in the `def evolve(self,ga)` function where `ga` is the `GAEngine` object. Return 1 from this function if the required fitness value is found else no need to return anything

```
from pygenetic import Evolution
class CustomEvolution(Evolution.BaseEvolution):
  def __init__(self,...):
    ....
    
  def evolve(self,ga):
    # Carry out custom evolution
    # Current population is at ga.population.members
    ### Note:
    ### ga.handle_selection() does the selection using the given selection handler
    ### Fitness mappings are present at ga.fitness_mappings
    ### ga.chooseCrossoverHandler() chooses 
    ### ga.doCrossover(crossoverHandler,father,mother) executes crossover
    ### ga.chooseMutationHandler() chooses 
    ### ga.doMutation(mutationHandler,chromosome) does mutation
    # Fill ga.population.new_members with the new population from evolution
    # Return 1 if the required fitness value is found else no need to return anything
```

## 2. Usage of `SimpleGA`: the High Level pygenetic GA API 

Very Simple GAs can be executed using `SimpleGA`

```
from pygenetic import SimpleGA
ga = SimpleGA.SimpleGA(minValue=1,maxValue=120,
                      noOfGenes=20,fitness_func=lambda x:sum(x),
                      duplicates=False,population_size=1000,
                      fitness_type='max')
```
where `minValue` is the minimum value a gene can take
      `maxValue` is the maximum value a gene can take
      `noOfGenes` is the number of genes in a chromosome
      `duplicates` determines if duplicates in the chromosome are allowed
      `fitness_func` is the fitness function
      `population_size` is the size of the population
      `fitness_type` is the fitness type (similar to `GAEngine`)
  
Other parameters include
* `cross_prob`: crossover probability
* `mut_prob`: mutation probability
* `crossover_handler`: can one of the the following values `'distinct'`, `'onePoint'`, `'twoPoint'`, `'PMX'` and `'OX'` ( default=`'onePoint'`)
* `mutation_handler`: can take one of the  following values `'swap'` and `'bitFlip'` ( default=`'swap'`)
* `selection_handler`: can take one of the  following values `'best'`, `'rank'` and `'roulette'` ( default=`'swap'`)

It can then be run
```
ga.evolve(10)
```
for evolving it for 10 generations

## 3. Best ANN Topology Finder

Users can find best ANN Topology to train for a classification problem using GA

```
from pygenetic import ANNEvolve 
import numpy
# load pima indians dataset
dataset = numpy.loadtxt("input.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
a = ANNEvolve.ANNTopologyEvolve(X,Y,hiddenLayers=2,population_size=10,
                          neuronsPerLayer=[2,5,10,12],activations=['relu','sigmoid'],
                          optimizers=['adam'],loss='binary_crossentropy',
                          metrics='accuracy',epochs=30,batch_size=10)
a.evolve(100)
print(a.best_fitness)
```

