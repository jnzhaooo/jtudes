from networkx.classes.digraph import DiGraph
from rFSA import rFSA
from FSA_run import FSA_obsrun, FSA_run

class rTwinPlant(DiGraph):
    def __init__(self, FSA):
        DiGraph.__init__(self, initial=set())
        for x in list(FSA.nodes):
            for y in list(FSA.nodes):
                self.add_node((x,y))
                self.graph['initial'].add((x,y))

        events = FSA.event_names

        FSA_reverse = rFSA(FSA)

        already_set = set()
        todo_list = list()
        for initial_node in self.graph['initial']:
            todo_list.append(initial_node)

        while len(todo_list)!=0:
            node = todo_list.pop()
            x = node[0]
            y = node[1]
            already_set.add(node)
            node_neighbors = set()
            for obs in FSA.symbol_names:
                x_nextstates = FSA_obsrun(FSA_reverse, x, obs)
                y_nextstates = FSA_obsrun(FSA_reverse, y, obs)
                if x_nextstates and y_nextstates:
                    for x_next in x_nextstates:
                        for y_next in y_nextstates:
                            self.add_edge(node, (x_next, y_next), event=(obs, obs))
                            node_neighbors.add((x_next, y_next))

            for event in events:
                if FSA.mask[event] == 'epsilon':
                    x_next = FSA_run(FSA_reverse, x, event)
                    y_next = FSA_run(FSA_reverse, y, event)
                    if x_next:
                        self.add_edge(node, (x_next, y), event=(event, 'epsilon'))
                        node_neighbors.add((x_next, y))
                    if y_next:
                        self.add_edge(node, (x, y_next), event=('epsilon', event))
                        node_neighbors.add((x, y_next))
            for neighbor in node_neighbors:
                if neighbor not in already_set:
                    todo_list.append(neighbor)
