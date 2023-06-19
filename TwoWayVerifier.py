from networkx.classes.digraph import DiGraph
from FSA_run import FSA_obsrun, FSA_run

class TwoWayVerifier(DiGraph):
    def __init__(self, FSA):
        DiGraph.__init__(self, initial=set())
        for x in FSA.graph['initial']:
            for y in FSA.graph['initial']:
                for z in FSA.nodes:
                    for w in FSA.nodes:
                        self.graph['initial'].add((x,y,z,w))
                        self.add_node((x,y,z,w))


        events = FSA.event_names

        already_set = set()
        todo_list = list()
        for initial_node in self.graph['initial']:
            todo_list.append(initial_node)

        while len(todo_list) != 0:
            node = todo_list.pop()
            x1 = node[0]
            x2 = node[1]
            x3 = node[2]
            x4 = node[3]

            already_set.add(node)
            node_neighbors = set()

            for obs in FSA.symbol_names:
                x1_nextstates = FSA_obsrun(FSA, x1, obs)
                x2_nextstates = FSA_obsrun(FSA, x2, obs)
                x3_nextstates = FSA_obsrun(FSA, x3, obs)
                x4_nextstates = FSA_obsrun(FSA, x4, obs)
                if x1_nextstates and x2_nextstates:
                    for x1_next in x1_nextstates:
                        for x2_next in x2_nextstates:
                            self.add_edge(node, (x1_next, x2_next, x3, x4), event=(obs, obs, 'epsilon', 'epsilon'))
                            node_neighbors.add((x1_next, x2_next, x3, x4))
                if x3_nextstates and x4_nextstates:
                    for x3_next in x3_nextstates:
                        for x4_next in x4_nextstates:
                            self.add_edge(node, (x1, x2, x3_next, x4_next), event=('epsilon', 'epsilon', obs, obs))
                            node_neighbors.add((x1, x2, x3_next, x4_next))
            for event in events:
                if FSA.mask[event] == 'epsilon':
                    x1_next = FSA_run(FSA, x1, event)
                    x2_next = FSA_run(FSA, x2, event)
                    x3_next = FSA_run(FSA, x3, event)
                    x4_next = FSA_run(FSA, x4, event)
                    if x1_next:
                        self.add_edge(node, (x1_next, x2, x3, x4), event=(event, 'epsilon', 'epsilon', 'epsilon'))
                        node_neighbors.add((x1_next, x2, x3, x4))
                    if x2_next:
                        self.add_edge(node, (x1, x2_next, x3, x4), event=('epsilon', event, 'epsilon', 'epsilon'))
                        node_neighbors.add((x1, x2_next, x3, x4))
                    if x3_next:
                        self.add_edge(node, (x1, x2, x3_next, x4), event=('epsilon', 'epsilon', event, 'epsilon'))
                        node_neighbors.add((x1, x2, x3_next, x4))
                    if x4_next:
                        self.add_edge(node, (x1, x2, x3, x4_next), event=('epsilon', 'epsilon', 'epsilon', event))
                        node_neighbors.add((x1, x2, x3, x4_next))
            for neighbor in node_neighbors:
                if neighbor not in already_set:
                    todo_list.append(neighbor)







                    
