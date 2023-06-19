def predictability_verification(TP, FSA):
    boundary_states = set()
    indicator_states = set()

    for state in list(FSA.nodes):
        for neighbor in list(FSA.successors(state)):
            if FSA.nodes[state]['fault'] == 'nf' and FSA.nodes[neighbor]['fault'] == 'f':
                boundary_states.add(state)

    length_delay = len(FSA.nodes) * len(FSA.nodes) + 2


    for x in list(FSA.nodes):
        if FSA.nodes[x]['fault'] == 'nf':
            reachable_states_for_x = reachable_states_after_k_steps(FSA, x, length_delay)
            binary_for_x = list()
            for state in reachable_states_for_x:
                if FSA.nodes[state]['fault'] == 'f':
                    binary_for_x.append(True)
                else:
                    binary_for_x.append(False)
            if all(binary_for_x):
                indicator_states.add(x)

    nonindicator_states = set()
    
    for x in list(FSA.nodes):
        if FSA.nodes[x]['fault'] == 'nf' and x not in indicator_states:
            nonindicator_states.add(x)

    for node in list(TP.nodes):
        if node[0] in boundary_states and node[1] in nonindicator_states:
            return False
    return True


def reachable_states_after_k_steps(FSA, state, k):
    reachable_states = set()
    todo_list = list()
    todo_list.append((state, 0))

    while len(todo_list) != 0:
        (node, length) = todo_list.pop()
        node_neighbors = list(FSA.successors(node))

        for neighbor in node_neighbors:
            length += 1
            if length < k:
                todo_list.append((neighbor, length))
            else:
                reachable_states.add(neighbor)

    return all_reachable_states(FSA, reachable_states)
        
def all_reachable_states(FSA, x_set):
    todo_list = list()
    already_set = set()

    for x in x_set:
        todo_list.append(x)

    while len(todo_list)!=0:
        state = todo_list.pop()
        already_set.add(state)
        state_neighbors = list(FSA.successors(state))
        for neighbor in state_neighbors:
            if neighbor not in already_set:
                todo_list.append(neighbor)
    return already_set
