def initial_state_opacity_verification(rOBS, FSA):
    nodes_robs = rOBS.nodes
    nodes_copy = list()
    nodes_initial_estimate = set()

    for node in nodes_robs:
        initial_state_estimate = set(node) & FSA.graph['initial']
        if initial_state_estimate:
            nodes_initial_estimate.add(tuple(initial_state_estimate))

    for node in nodes_initial_estimate:
        estimate_for_node = list()
        for x in set(node):
            if FSA.nodes[x]['secret'] == 's':
                estimate_for_node.append(True)
            else:
                estimate_for_node.append(False)
        nodes_copy.append(tuple(estimate_for_node))

    for estimate in nodes_copy:
        if all(estimate):
            return False
    return True
