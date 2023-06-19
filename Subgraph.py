from networkx.classes.digraph import DiGraph


class Subgraph(DiGraph):
    def __init__(self, FSA, initial_states, state_list):
        DiGraph.__init__(self, initial=set())
        for x in initial_states:
            self.graph['initial'].add(x)

        for x in state_list:
            self.add_node(x)

        for x in state_list:
            for y in state_list:
                if (x, y) in list(FSA.edges):
                    self.add_edge(x, y, event=FSA.edges[(x,y)]['event'], obs=FSA.edges[(x,y)]['obs'])
