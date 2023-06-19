def infinite_step_opacity_verification(rOBS, OBS, FSA):
    nodes_obs = OBS.nodes
    nodes_robs = rOBS.nodes
    nodes_copy = list()
    nodes_delay_estimate = set()

    for node_1 in nodes_obs:
        for node_2 in nodes_robs:
            delay_state_estimate = set(node_1) & set(node_2)
            if delay_state_estimate:
                nodes_delay_estimate.add(tuple(delay_state_estimate))

    for node in nodes_delay_estimate:
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
