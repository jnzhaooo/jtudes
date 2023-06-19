def FSA_run(FSA, state, event):
    for successor in FSA.successors(state):
        if FSA.edges[(state, successor)]['event'] == event:
            return successor



def FSA_obsrun(FSA, state, obs):
    next_states = set()
    for successor in FSA.successors(state):
        if FSA.edges[(state, successor)]['obs'] == obs:
            next_states.add(successor)
    return next_states







