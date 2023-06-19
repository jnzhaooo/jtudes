def opacity_verification(OBS, FSA):
    nodes_obs = OBS.nodes
    nodes_copy = list()
    for node in nodes_obs:
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
