from cycle_detection import TarjansAlgorithm, is_self_loop

def I_detectability_verification(rTP, FSA):
    tarjan = TarjansAlgorithm(rTP)
    all_scc = tarjan.strongly_connected_components(list(rTP.nodes)[0])
    
    scc_to_delete = list()
    for scc in all_scc:
        if len(scc) == 1 and is_self_loop(scc[0][0], rTP) == False:
            scc_to_delete.append(scc)
    
    for scc in scc_to_delete:
        all_scc.remove(scc)

    for scc in all_scc:
        for node in scc:
            pair = node[0]
            if pair[0] != pair[1]:
                return False
    return True
