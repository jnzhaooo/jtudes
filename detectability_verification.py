from cycle_detection import TarjansAlgorithm, is_self_loop

def detectability_verification(TP, FSA):
    tarjan = TarjansAlgorithm(TP)
    all_scc = tarjan.strongly_connected_components(list(TP.nodes)[0])
    
    scc_to_delete = list()
    for scc in all_scc:
        if len(scc) == 1 and is_self_loop(scc[0][0], TP) == False:
            scc_to_delete.append(scc)
    
    for scc in scc_to_delete:
        all_scc.remove(scc)

    for scc in all_scc:
        for node in scc:
            pair = node[0]
            if pair[0] != pair[1]:
                return False
    return True
