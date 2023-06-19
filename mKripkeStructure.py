from networkx.classes.digraph import DiGraph

class mKripkeStructure(DiGraph):
    def __init__(self, KS):
        DiGraph.__init__(self, initial=set())
        nodes_ks = KS.nodes
        for p in nodes_ks:
            for q in nodes_ks:
                if (p,q) in list(KS.edges):
                    self.add_edge(p, q)
        
        self.symbol_names = KS.symbol_names
        self.secret_states = KS.secret_states
        self.initial_states = KS.initial_states
        self.fault_states = KS.fault_states

        self.graph['initial'] = KS.graph['initial']

        
        for state in nodes_ks:
            state_copy = (state[0], 'tau', state[1])
            self.add_edge(state, state_copy)
            self.add_edge(state_copy, state)
