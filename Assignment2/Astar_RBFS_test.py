import random
import time
import numpy

import RBFS, Problem, astar
from utils import *


#8 puzzle
eight_Puzzle= [1, 0, 3, 4, 5, 8, 2, 6, 7]

astar.astar_search(Problem.EightPuzzle(tuple(eight_Puzzle)))
nodesA = astar.getNCount()
print("The notes of A* in 8-puzzle is:") 
print(nodesA)

RBFS.recursive_best_first_search(Problem.EightPuzzle(tuple(eight_Puzzle)))
nodesR = RBFS.getNCount()
print("The nodes of RBFS in 8-puzzle is:") 
print(nodesR)

#TSP
size = 10
map = init_matrix(numpy.random.random((size, 2)))

astar.astar_search(Problem.TSP((3,), map, list(range(size))))
nodesA = astar.getNCount()
print("The notes of A* in TSP is:") 
print(nodesA)

RBFS.recursive_best_first_search(Problem.TSP((3,), map, list(range(size))))
nodesR = RBFS.getNCount()
print("The nodes of RBFS in TSP is:") 
print(nodesR)

