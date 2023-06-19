from Subgraph import Subgraph

def is_self_loop(vertex, g):
    for successor in g.successors(vertex):
        if successor == vertex:
            return True
    return False


class TarjansAlgorithm:
    def __init__(self, g):
        self.g = g
        self._result = list()
        self._vertices = list(g.nodes)
        self._size = len(self._vertices)
        self._disc = [-1] * self._size
        self._low = [-1] * self._size
        self._OnStack = [False] * self._size
        self._st = list()

    
    def strongly_connected_components(self, initial):

        time = 0
        DFS_vertices = self.DFS(initial)
        order = range(0, self._size)
        id_dict = dict(zip(DFS_vertices, order))
        for i in range(0, self._size):
            if self._disc[i] == -1:
                self._scc_util(i, time, id_dict, DFS_vertices)
        return self._result


    def _scc_util(self, i, time, id_dict, DFS_vertices):
        self._disc[i] = time
        self._low[i] = time
        time += 1
        self._OnStack[i] = True
        self._st.append(i)
        try:
            self.g.successors(DFS_vertices[i])
        except:
            pass
        else:
            for v in self.g.successors(DFS_vertices[i]):
                if self._disc[id_dict.get(v, -1)] == -1:
                    self._scc_util(id_dict.get(v), time, id_dict, DFS_vertices)
                    self._low[i] = min(self._low[i], self._low[id_dict.get(v)])
                elif self._OnStack[id_dict.get(v)] == True:
                    self._low[i] = min(self._low[i], self._disc[id_dict.get(v)])
            w = -1
            if self._low[i] == self._disc[i]:
                scc = list()
                while w != i:
                    w = self._st.pop()
                    scc.append((DFS_vertices[w],w))
                    self._OnStack[w] = False
                self._result.append(scc)


    def DFS(self, initial):
        d = list()
        visited = set()
        self._DFSUtil(initial, visited, d)
        for v in self._vertices:
            if v not in visited:
                self._DFSUtil(v, visited, d)
        return d



    def _DFSUtil(self, v, visited, d):
        d.append(v)
        visited.add(v)
        for neighbor in list(self.g.successors(v)):
            if neighbor not in visited:
                self._DFSUtil(neighbor, visited, d)



class JohnsonsAlgorithm:
    def __init__(self, g):
        self.g = g
        self.blocked_set = set()
        self.blocked_map = dict()
        self.stack = list()
        self.all_cycles = list()
        self.vertices = list(g.nodes)


    def simple_cycles(self, g):
        start_index = 0
        initial = TarjansAlgorithm(g)
        DFS_vertices = initial.DFS(self.vertices[0])
        while start_index <= len(self.vertices)-1:
            subgraph = self.create_sub_graph(start_index, g, DFS_vertices)
            tarjan = TarjansAlgorithm(subgraph)
            scc_graphs = tarjan.strongly_connected_components(DFS_vertices[start_index])
            least_vertex = self.find_least_vertex(scc_graphs)
            if least_vertex[0] != None:
                self.blocked_set.clear()
                self.blocked_map.clear()
                val = self.simple_cycles_util(least_vertex[0], least_vertex[0])
                start_index = DFS_vertices.index(least_vertex[0]) + 1
            else:
                break
        for v in self.vertices:
            if is_self_loop(v, g):
                self.all_cycles.append([v,v])
        return self.all_cycles


    def create_sub_graph(self, index, g, DFS_vertices):
        initial_states = list()
        initial_states.append(DFS_vertices[index])
        state_list = DFS_vertices[index:]

        result = Subgraph(g, initial_states, state_list)
        
        return result


    def find_least_vertex(self, subgraphs):
        min_id = 99999999
        min_vertex = None
        for graph in subgraphs:
            if len(graph) == 1:
                continue
            else:
                for v in graph:
                    if v[1] < min_id:
                        min_vertex = v[0]
                        min_id = v[1]
        return (min_vertex, min_id)


    def simple_cycles_util(self, start, current):
        foundCycle = False
        self.stack.append(current)
        self.blocked_set.add(current)

        for neighbor in self.g.successors(current):
            if neighbor == start:
                self.stack.append(start)
                cycle = list()
                cycle.extend(self.stack)
                self.stack.pop()
                self.all_cycles.append(cycle)
                foundCycle = True
            elif neighbor not in self.blocked_set:
                gotcycle = self.simple_cycles_util(start, neighbor)
                foundCycle = gotcycle or foundCycle

        if foundCycle == True:
            self.unblock(current)
        else:
            for neighbor in self.g.successors(current):
                if self.blocked_map.get(neighbor, -1) == -1:
                    self.blocked_map[neighbor] = [current]
                else:
                    self.blocked_map[neighbor].append(current)
        if len(self.stack) > 0:
            self.stack.pop()
        return foundCycle



    def unblock(self, vertex):
        self.blocked_set.remove(vertex)
        if self.blocked_map.get(vertex,-1) != -1:
            for v in self.blocked_map.get(vertex):
                if v in self.blocked_set:
                    self.unblock(v)
            self.blocked_map.pop(vertex)

