from cycle_detection import TarjansAlgorithm, is_self_loop

def weak_detectability_verification(OBS, FSA):
    tarjan = TarjansAlgorithm(OBS)
    all_scc = tarjan.strongly_connected_components(list(OBS.nodes)[0])

    scc_to_delete = list()
    for scc in all_scc:
        if len(scc) == 1 and is_self_loop(scc[0][0], OBS) == False:
            scc_to_delete.append(scc)

    for scc in scc_to_delete:
        all_scc.remove(scc)

    for scc in all_scc:
        binary_for_scc = list()
        for node in scc:
            state_obs = node[0]
            if len(state_obs) == 1:
                binary_for_scc.append(True)
            else:
                binary_for_scc.append(False)
        if all(binary_for_scc):
            return True
    return False

