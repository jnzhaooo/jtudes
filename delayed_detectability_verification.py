from cycle_detection import TarjansAlgorithm, is_self_loop

def delayed_detectability_verification(TW, FSA):
    reachable_nodes = set()
    
    delay_length = len(FSA.nodes) * len(FSA.nodes) + 2
    observation_length = 1


    todo_list = list()
    already_set = set()

    for initial_node in TW.graph['initial']:
        todo_list.append((initial_node, 0, 0))

    while len(todo_list) != 0:
        (node, len_for_obs, len_for_delay) = todo_list.pop()
        already_set.add((node, len_for_obs, len_for_delay))

        node_neighbors = list(TW.successors(node))
        for neighbor in node_neighbors:
            if TW.edges[(node, neighbor)]['event'][0] != 'epsilon':
                len_for_obs += 1
            if TW.edges[(node, neighbor)]['event'][2] != 'epsilon':
                len_for_delay += 1
            if len_for_obs < observation_length and len_for_delay < delay_length and (neighbor, len_for_obs, len_for_delay) not in already_set:
                todo_list.append((neighbor, len_for_obs, len_for_delay))
            else:
                reachable_nodes.add(neighbor)

    for node in all_reachable_nodes(TW, reachable_nodes):
        if node[0] == node[2] and node[1] == node[3]:
            if node[0] != node[1] or node[2] != node[3]:
                return False
    return True



def all_reachable_nodes(TW, reachable_nodes):
    todo_list = list()
    already_set = set()
    for node in reachable_nodes:
        todo_list.append(node)

    while len(todo_list) != 0:
        node = todo_list.pop()
        already_set.add(node)
        node_neighbors = list(TW.successors(node))
        for neighbor in node_neighbors:
            if neighbor not in already_set:
                todo_list.append(neighbor)
    return already_set
