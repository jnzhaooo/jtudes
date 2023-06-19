from cycle_detection import TarjansAlgorithm, is_self_loop

def diagnosability_verification(TP, FSA):
    tarjan = TarjansAlgorithm(TP)
    all_scc = tarjan.strongly_connected_components(list(TP.nodes)[0])
    
    scc_to_delete = list()
    for scc in all_scc:
        if len(scc) == 1 and is_self_loop(scc[0][0], TP) == False:
            scc_to_delete.append(scc)
    
    for scc in scc_to_delete:
        all_scc.remove(scc)

    for scc in all_scc:
        binary_for_scc = list()
        for node in scc:
            pair = node[0]
            if FSA.nodes[pair[0]]['fault'] != FSA.nodes[pair[1]]['fault']:
                binary_for_scc.append(True)
            else:
                binary_for_scc.append(False)
        if all(binary_for_scc):
            return False
    return True
