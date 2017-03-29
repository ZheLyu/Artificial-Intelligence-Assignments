import random

import numpy

import  Problem, genetic
from utils import *

# generate TSP problem
size = 5
loc = list(range(size))
start = random.randint(0, size - 1)
map = init_matrix(numpy.random.random((size, 2)))
print("size=%s" % (size))

# genetic algorithm
ga_result = genetic.genetic_algorithm(loc, map, 2000, 10)
print("Genetic algorithm's optional result is %s and the order is %s" % (ga_result[0], ga_result[1]))