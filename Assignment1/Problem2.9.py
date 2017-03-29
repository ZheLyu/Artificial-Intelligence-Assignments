import random
import collections

class Thing(object):

    def __repr__(self):
        return '<{}>'.format(getattr(self, '__name__', self.__class__.__name__))

    def is_alive(self):
        return hasattr(self, 'alive') and self.alive

    def show_state(self):
        print("I don't know how to show_state.")

class Agent(Thing):

    def __init__(self, program=None):
        self.alive = True
        self.bump = False
        self.holding = []
        self.performance = 0
        if program is None:
            def program(percept):
                return eval(input('Percept={}; action? ' .format(percept)))
        assert isinstance(program, collections.Callable)
        self.program = program

loc_A, loc_B = (0, 0), (1, 0) 

def ReflexVacuumAgent():
   
    model = {loc_A: None, loc_B: None}

    def program(percept):
        location, status = percept
        model[location] = status  # Update the model here
        if model[loc_A] == model[loc_B] == 'Clean':
            return 'NoOp'
        elif status == 'Dirty':
            return 'Suck'
        elif location == loc_A:
            return 'Right'
        elif location == loc_B:
            return 'Left'
    return Agent(program)

class Environment(object):

    def __init__(self):
        self.things = []
        self.agents = []

    def thing_classes(self):
        return []  

    def percept(self, agent):
      
        raise NotImplementedError

    def execute_action(self, agent, action):
        raise NotImplementedError

    def default_location(self, thing):
        return None

    def exogenous_change(self):
        pass

    def is_done(self):
        return not any(agent.is_alive() for agent in self.agents)

    def step(self):    
        if not self.is_done():
            actions = []
            for agent in self.agents:
                if agent.alive:
                    actions.append(agent.program(self.percept(agent)))
                else:
                    actions.append("")
            for (agent, action) in zip(self.agents, actions):
                self.execute_action(agent, action)
            self.exogenous_change()
    
class TrivialVacuumEnvironment(Environment):

    def __init__(self):
        super(TrivialVacuumEnvironment, self).__init__()
        self.status = {loc_A: random.choice(['Clean', 'Dirty']),
                       loc_B: random.choice(['Clean', 'Dirty'])}

    def percept(self, agent):
        print (agent.location, self.status[agent.location])
        return (agent.location, self.status[agent.location])

    def execute_action(self, agent, action): 
        if action == 'Right':
            print 'Right'
            agent.location = loc_B
            agent.performance -= 1

        elif action == 'Left':
            print 'Left'
            agent.location = loc_A
            agent.performance -= 1
        elif action == 'Suck':
            print 'Suck'
            if self.status[agent.location] == 'Dirty':
                agent.performance += 10
            self.status[agent.location] = 'Clean'
        print(agent.performance)

    def default_location(self, thing):
        return random.choice([loc_A, loc_B])

    def run(self, steps=1000):
        for step in range(steps):
            if self.is_done():
                return
            self.step()

    def add_thing(self, thing, location=None):
 
        if not isinstance(thing, Thing):
            thing = Agent(thing)
        assert thing not in self.things
        thing.location = location if location is not None else self.default_location(thing)
        self.things.append(thing)
        if isinstance(thing, Agent):
            thing.performance = 0
            self.agents.append(thing)

e = TrivialVacuumEnvironment()
e.add_thing(ReflexVacuumAgent())
e.run(5)

