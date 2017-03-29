import random

import numpy

import hill_climbing, Problem, astar
from utils import *
size = 5
loc = list(range(size))
start = random.randint(0, size - 1)
map = init_matrix(numpy.random.random((size, 2)))
print("size=%s" % (size))

astar_result = astar.astar_search(Problem.TSP((start,), map, loc))
distance = astar_result.path_cost
state = astar_result.state
print("A star' optional result is %s and the order is %s" % (distance, str(state)))

hc_result = hill_climbing.hill_climb(2000, loc, map)
print("Hill-climbing's optional result is %s and the order is %s" % (hc_result[0], hc_result[1]))

size = 10
loc = list(range(size))
start = random.randint(0, size - 1)
map = init_matrix(numpy.random.random((size, 2)))
print("size=%s" % (size))

astar_result = astar.astar_search(Problem.TSP((start,), map, loc))
distance = astar_result.path_cost
state = astar_result.state
print("A star' optional result is %s and the order is %s" % (distance, str(state)))

hc_result = hill_climbing.hill_climb(2000, loc, map)
print("Hill-climbing's optional result is %s and the order is %s" % (hc_result[0], hc_result[1]))

size = 20
loc = list(range(size))
start = random.randint(0, size - 1)
map = init_matrix(numpy.random.random((size, 2)))
print("size=%s" % (size))

astar_result = astar.astar_search(Problem.TSP((start,), map, loc))
distance = astar_result.path_cost
state = astar_result.state
print("A star' optional result is %s and the order is %s" % (distance, str(state)))

hc_result = hill_climbing.hill_climb(2000, loc, map)
print("Hill-climbing's optional result is %s and the order is %s" % (hc_result[0], hc_result[1]))
