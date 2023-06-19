from networkx.classes.digraph import DiGraph
from ureach import ureach_from_state
from observable_transition import obsnext_from_state

class KripkeStructure(DiGraph):
    def __init__(self, FSA):
        DiGraph.__init__(self, initial=set())
        nodes_ks = list()
        for x in FSA.nodes:
            for obs in FSA.symbol_names:
                nodes_ks.append((x, obs))
        for x in FSA.nodes:
            nodes_ks.append((x, 'epsilon'))

        initial_states_ks = set()
        for initial_x in FSA.graph['initial']:
            for x in ureach_from_state(FSA, initial_x):
                initial_states_ks.add((x, 'epsilon'))

        
        already_set = set()
        todo_list = list()
        for initial_q in initial_states_ks:
            todo_list.append(initial_q)

        while len(todo_list)!=0:
            state = todo_list.pop()
            already_set.add(state)
            state_neighbors = set()
            for next_state in nodes_ks:
                if next_state[1] in FSA.symbol_names and next_state[0] in obsnext_from_state(FSA, state[0], next_state[1]):
                    self.add_edge(state, next_state)
                    state_neighbors.add(next_state)
            for neighbor in state_neighbors:
                if neighbor not in already_set:
                    todo_list.append(neighbor)

        for initial_state in initial_states_ks:
            if initial_state in self.nodes:
                self.graph['initial'].add(initial_state)


        self.symbol_names = FSA.symbol_names
        self.secret_states = FSA.secret_states
        self.initial_states = list(FSA.graph['initial'])
        self.fault_states = FSA.fault_states
