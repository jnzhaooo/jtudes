from networkx.classes.digraph import DiGraph
from powerset import powerset
from ureach import ureach_from_state
from ureach import ureach_from_set
from observable_transition import obsnext


class OBS(DiGraph):
    def __init__(self, FSA):
        DiGraph.__init__(self, initial=tuple())
        node_obs = list(powerset(FSA.nodes))
        node_obs.remove(())
        transitions_obs = set()
        for item in list(FSA.edges):
            obs = FSA.edges[item]['obs']
            if obs != 'epsilon':
                transitions_obs.add(obs)
        initial_obs = set()
        for initial_state in FSA.graph['initial']:
            initial_obs = initial_obs | ureach_from_set(FSA, initial_state)
            
        self.graph['initial']=tuple(initial_obs)
        self.add_node(self.graph['initial'])


        already_set = set()
        todo_list = list()
        todo_list.append(self.graph['initial'])
        while len(todo_list)!=0:
            ns = todo_list.pop()
            already_set.add(ns)
            ns_neighbors = set()
            for y in node_obs:
                for obs in transitions_obs:
                    if set(y) == obsnext(FSA, set(ns), obs):
                        self.add_edge(tuple(ns), tuple(y), obs=obs)
                        ns_neighbors.add(y)
            for neighbor in ns_neighbors:
                if neighbor not in already_set:
                    todo_list.append(neighbor)











