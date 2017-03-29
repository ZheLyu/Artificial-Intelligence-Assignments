import sys

from utils import *
NCOUNT = 0

def getNCount():
    global NCOUNT
    tmp = NCOUNT
    NCOUNT = 0
    return tmp

def recursive_best_first_search(problem, h=None):

    h = memoize(h or problem.h, 'h')

    def RBFS(problem, node, flimit):
        global NCOUNT
        if problem.goal_test(node.state):
            return node, 0   # (The second value is immaterial)
        successors = node.expand(problem)
        if len(successors) == 0:
            return None, sys.maxsize
        for s in successors:
            s.f = max(s.path_cost + h(s), node.f)    
        while True:
            # Order by lowest f value
            NCOUNT=NCOUNT+1
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > flimit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = sys.maxsize
            result, best.f = RBFS(problem, best, min(flimit, alternative))
            if result is not None:
                return result, best.f            
    
    node = Node(problem.initial)
    node.f = h(node)
    result, bestf = RBFS(problem, node, sys.maxsize)
    return result


