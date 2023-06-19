from networkx.classes.digraph import DiGraph

class rFSA(DiGraph):
    def __init__(self, FSA):
        DiGraph.__init__(self, initial=set())
        nodes = FSA.nodes
        self.graph['initial'] = set(nodes)

        for x in nodes:
            self.add_node(x)

        for x in nodes:
            for y in nodes:
                if (x,y) in FSA.edges:
                    event_name = FSA.edges[(x,y)]['event']
                    event_obs = FSA.edges[(x,y)]['obs']
                    self.add_edge(y, x, event=event_name, obs=event_obs)
