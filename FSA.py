from networkx.classes.digraph import DiGraph


class FSA(DiGraph):
    def __init__(self, node_list, init_nodes, edge_list):
        DiGraph.__init__(self, initial=set())
        for item in node_list:
            self.add_node(item[0],secret=item[1],fault=item[2])
            if item[0] in init_nodes:
                self.graph['initial'].add(item[0])

        for edge in edge_list:
            self.add_edge(edge[0],edge[1],event=edge[2],obs=edge[3])            

        self.symbol_names = list()
        names = set()
        for edge in edge_list:
            if edge[3] != 'epsilon':
                names.add(edge[3])
        self.symbol_names = list(names)

        self.secret_states = list()
        secret = set()
        for state in node_list:
            if state[1] == 's':
                secret.add(state[0])
        self.secret_states = list(secret)

        self.fault_states = list()
        fault = set()
        for state in node_list:
            if state[2] == 'f':
                fault.add(state[0])
        self.fault_states = list(fault)

        self.event_names = list()
        events = set()
        for edge in edge_list:
            events.add(edge[2])
        self.event_names = list(events)

        self.mask = dict()
        for edge in edge_list:
            self.mask[edge[2]] = edge[3]
