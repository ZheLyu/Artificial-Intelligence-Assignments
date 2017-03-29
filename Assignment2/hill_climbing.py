import random
import sys

from utils import *


# Connect all cities into random path and divide the path into three parts
# Try all the combinations and select the one with lowest path-cost as "Climbing hills"
def hill_climb(repeat_times, loc, map):
    def hc(loc, graph):
        locations = list(range(len(loc)))
        random.shuffle(locations)
        breakpoints = random.sample(range(1, len(loc)), 2)
        breakpoints.sort()
        ran1 = locations[:breakpoints[0]]
        ran2 = locations[breakpoints[0]:breakpoints[1]]
        ran3 = locations[breakpoints[1]:]
        rans = [ran1, ran2, ran3]

        result = sys.maxsize
        result_order = []
        for i in rans:
            for j in rans:
                for k in rans:
                    if i != j and j != k and i != k:
                        temp = cal_length(i + j + k, graph)
                        if temp < result:
                            result_order = i + j + k
                            result = temp
        result_order.append(result_order[0])
        return result, result_order

    result = sys.maxsize
    result_tuple = ()
    while repeat_times > 0:
        temp = hc(loc, map)
        if temp[0] < result:
            result_tuple = temp
            result = temp[0]
        repeat_times -= 1
    return result_tuple