# pygenetic: An Efficient Generic, User-friendly Python Genetic Algorithm API
[![Build Status](https://travis-ci.com/danny311296/pygenetic.svg?token=A3bcYHcDEvK23esetBsC&branch=master)](https://travis-ci.com/danny311296/pygenetic) [![MIT Licence](https://badges.frapsoft.com/os/mit/mit.svg?v=103)](https://opensource.org/licenses/mit-license.php)  [![docs](https://readthedocs.org/projects/pygenetic/badge/?version=latest)](https://pygenetic.readthedocs.io/en/latest/?badge=latest)

pygenetic is a Python Genetic Algorithm API which is User-Friendly as well as Generic in nature unlike most GA APIs which make a trade off between the two.

## Motivation
![alt text](https://github.com/danny311296/pygenetic/blob/phase1/reports/imgs/motivation.png)
While some APIs like DEAP and many more recent ones which are very efficient and generic are less user friendly in nature, other APIs like genetics and other smaller ones which are the best in terms of user friendliness, they are less generic. This API intends to strike a balance - good in terms of both user friendliness and genericity.

## Features
* Presence of both High-Level(`SimpleGA`) and Low-Level API(`GAEngine`) which users can use as per need.
* Very generic API - Users can customize different part of the GA be it Evolution, Statistics, Different handlers, Chromosome Representations.
* Supports efficient evolution execution using Apache Spark. This is highly scalable as more workers can be deployed. Parallelization of fitness evaluation, selection, crossovers and mutations are taken care of.
* Supports Adaptive Mutation Rates based on how diverse the population is.
* Supports Hall of Fame(best ever chromosome) Injection so that the best chromosome isn't lost in later generations due to the selection method used.
* Supports Efficient Iteration Halt 
* Supports Visualization of Statistics like max, min, avg, diversity of fitnesses, mutation rates. Users can also define custom statistics
* Supports usage of multiple crossovers and mutations in one GA execution to enhance diversity
* Supports Population Control(control the population size or allow it grow/shrink) which users can make use of in various research purposes
* Provides a bunch of Standard Selection, Crossovers, Mutations and Fitness Functions
* Provides continue evolve feature so users can continue from previous evolutions instead of starting all over again.
* Provides ANN Best Topology finder using GA functionality

## Installation

pygenetic is published on pypi(https://pypi.org/project/pygenetic/) and can be easily installed by:

```sh
$ pip3 install pygenetic
```

For using pyspark functionality, install `pyspark` , Apache Spark, Scala and JVM.
For using the ANN Topology Finder, install `tensorflow` and `keras` 

## Tests

The various tests are present in the `tests/` directory. The main API tests can tested by:

```sh
$ pytest tests/modules
```

## Usage

### High Level API Basic Usage

```
from pygenetic import SimpleGA
ga = SimpleGA.SimpleGA(minValue=1,maxValue=120,
                      noOfGenes=20,fitness_func=lambda x:sum(x),
                      duplicates=False,population_size=1000,
                      fitness_type='max')
ga.evolve(100)
print(ga.best_fitness)
``` 

### Low Level API Basic Usage

```
from pygenetic import ChromosomeFactory, GAEngine, Utils
factory = ChromosomeFactory.ChromosomeRangeFactory(
			noOfGenes=8,minValue=1,maxValue=8)
ga = GAEngine.GAEngine(factory,100,fitness_type=('equal',8)
						,mut_prob = 0.3)
ga.addCrossoverHandler(Utils.CrossoverHandlers.distinct)
ga.addMutationHandler(Utils.MutationHandlers.swap)
ga.setSelectionHandler(Utils.SelectionHandlers.best)
ga.setFitnessHandler(Utils.Fitness.addition)
ga.evolve(10)
print(ga.best_fitness)
```

### For more advanced usages and tutorials

 Our python package is extensively documented on [ReadTheDocs](https://pygenetic.readthedocs.io/en/latest). Also, refer [this](https://github.com/danny311296/pygenetic/blob/master/examples/tutorial.md) for step by step tutorials.

 Refer `examples` for examples of solving different GAs using pygenetic

## GA Online Execution
 Install python `flask` and run
 ```sh
$ python3 flask/views.py
```
Input all the various fields needed for the GA. You can run the GA online and get the best 5 chromosomes of each generations followed by statistics. You can also download the equivalent pygenetic code based on all user inputs in the form

## Authors
* [Bharatraj S Telkar](https://github.com/BharatRajT) 
* [Daniel Isaac](https://github.com/danny311296) 
* [Shreyas V Patil](https://github.com/pshreyasv100)

## Special Mentions
* Special thanks to Ganesh K, Rahul Bhardwaj and Hardik Surana who lended their UI made for their Design Patterns project (https://github.com/ganesh-k13/GOF-Templates) as an intial template for us to work on for our Web GUI. 
* Special thanks to our Project Guide Prof.Chitra G M

### License: MIT
