import copy
import sys
from heapq import *

from utils import *


class Problem(object):
    """The abstract class for a formal problem.  You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions."""

    def __init__(self, initial, goal=None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal.  Your subclass's constructor can add
        other arguments."""
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        """Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once."""
        raise NotImplementedError

    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        raise NotImplementedError

    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough."""
        if isinstance(self.goal, list):
            return self.is_in(state, self.goal)
        else:
            return state == self.goal

    def is_in(self, elt, seq):
        """Similar to (elt in seq), but compares with 'is', not '=='."""
        return any(x is elt for x in seq)

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c + 1

    def value(self, state):
        """For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value."""
        raise NotImplementedError


class EightPuzzle(Problem):
    def __init__(self, initial, goal=None):
        super().__init__(initial, goal)
        self.initial = initial
        self.goal = goal

    def actions(self, stat):
        state = self.trans(stat)
        result = []
        p = -1
        q = -1
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    p = i
                    q = j
                    break

        for i in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            x = p + i[0]
            y = q + i[1]
            if 2 >= x >= 0 and 2 >= y >= 0:
                result.append(i)
        return result

    def trans(self, state):
        result = []
        count = 0
        for i in range(3):
            temp = []
            for j in range(3):
                temp.append(state[count])
                count += 1
            result.append(temp)
        return result

    def result(self, stat, action):
        state = self.trans(stat)
        temp = copy.deepcopy(state)
        p = -1
        q = -1
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] == 0:
                    p = i
                    q = j
                    break
        temp[p][q] = state[p + action[0]][q + action[1]]
        temp[p + action[0]][q + action[1]] = 0
        result = [x for sublist in temp for x in sublist]
        return tuple(result)

    def goal_test(self, stat):
        state = self.trans(stat)
        counter = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if state[i][j] != counter:
                    return False
                counter += 1
        return True

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def h(self, node):
        state = self.trans(node.state)
        result = 0
        for i in range(len(state)):
            for j in range(len(state[0])):
                if i == len(state) - 1 and j == len(state[0]) - 1:
                    break
                pos = state[i][j] // 3, state[i][j] % 3
                result += abs(pos[0] - i) + abs(pos[1] - j)
        print(result)
        return result


class TSP(Problem):

    def __init__(self, initial, map, places, goal=None):
        super().__init__(initial, goal)
        self.initial = initial
        self.goal = goal
        self.map = map
        self.places = places

    def actions(self, state):
        result = []
        for i in self.places:
            if i not in state:
                result.append(i)
        if len(result) == 0:
            result.append(state[0])
        return result

    def result(self, state, action):
        state = state + (action,)
        return state

    def goal_test(self, state):
        return len(state) == len(self.places) + 1

    def path_cost(self, c, state1, action, state2):
        l = len(state2)
        return c + self.map[state2[l - 2], state2[l - 1]]

    # heuristic function is to calculate the value of MST of rest node plus the current node to the nearest node on MST
    # and nearest node on MST to the source, which is a good estimation of the rest path-cost
    def h(self, node):
        loc = self.actions(node.state)
        if len(loc) == 1:
            if loc[0] == node.state[0]:
                return 0
            else:
                return self.map[loc[0], node.state[0]]
        shortest_self = sys.maxsize
        shortest_target = sys.maxsize
        for i in loc:
            if i != self.initial[0] and self.map[i, self.initial[0]] < shortest_target:
                shortest_target = self.map[i, self.initial[0]]
            if i != node.state[-1] and self.map[i, node.state[-1]] < shortest_self:
                shortest_self = self.map[i, node.state[-1]]
        edges = self.gen_edge(loc)
        heap = []
        result = 0
        for i in edges:
            heappush(heap, (self.map[i], i))
        uf = UnionFind(loc)
        while len(heap) != 0:
            edge = heappop(heap)[1]
            seta = self.find(uf, edge[0])
            setb = self.find(uf, edge[1])
            if seta != setb:
                result += self.map[edge]
                self.union(uf, seta, setb)

        return result + shortest_self + shortest_target

    @staticmethod
    def gen_edge(loc):
        edges = []
        for i in loc:
            for j in loc:
                if i != j:
                    edges.append((i, j))
        return edges

    @staticmethod
    def find(uf, s):
        return uf.group[s]

    @staticmethod
    def union(uf, a, b):
        if uf.size[a] > uf.size[b]:
            a, b = b, a
        for s in uf.items[a]:
            uf.group[s] = b
            uf.items[b].append(s)
        uf.size[b] += uf.size[a]
        del uf.size[a]
        del uf.items[a]
