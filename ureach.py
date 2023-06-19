from networkx.classes.digraph import DiGraph

def ureach_from_state(FSA, x):
    already_set = set()
    todo_list = list()
    todo_list.append(x)
    while len(todo_list)!=0:
        ns = todo_list.pop()
        already_set.add(ns)
        ns_neighbors = list(FSA.successors(ns))
        ur_of_ns = set()
        if ns_neighbors != list():
            for ns_succ in ns_neighbors:
                if FSA.edges[(ns,ns_succ)]['obs'] == 'epsilon':
                    ur_of_ns.add(ns_succ)
        if ur_of_ns != set():
            for neighbor in ur_of_ns:
                if neighbor not in already_set:
                    todo_list.append(neighbor)
    return already_set

def ureach_from_set(FSA, x_set):
    ur_of_x_set = set()
    for x in x_set:
        ur_of_x_set = ur_of_x_set | ureach_from_state(FSA, x)
    return ur_of_x_set
